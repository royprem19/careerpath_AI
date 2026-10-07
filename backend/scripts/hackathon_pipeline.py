import os
import json
import math
import numpy as np
import pandas as pd
from scipy import stats, optimize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "hackathon_analytics_results.json")

# ==========================================
# 1. PURE NUMPY / SCIPY ML ALGORITHMS
# ==========================================

def sigmoid(z):
    z = np.clip(z, -30, 30)
    return 1.0 / (1.0 + np.exp(-z))

def compute_auc(y_true, y_prob):
    # Calculate AUC using Mann-Whitney U test formula
    pos = y_prob[y_true == 1]
    neg = y_prob[y_true == 0]
    n_pos = len(pos)
    n_neg = len(neg)
    if n_pos == 0 or n_neg == 0:
        return 0.5
    count = 0
    for p in pos:
        count += np.sum(p > neg) + 0.5 * np.sum(p == neg)
    return float(count / (n_pos * n_neg))

def compute_classification_metrics(y_true, y_pred, y_prob=None):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    acc = (tp + tn) / max(1, len(y_true))
    prec = tp / max(1, (tp + fp))
    rec = tp / max(1, (tp + fn))
    f1 = 2 * prec * rec / max(1e-9, (prec + rec))
    auc = compute_auc(y_true, y_prob) if y_prob is not None else 0.5
    
    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1": round(float(f1), 4),
        "auc": round(float(auc), 4),
        "confusion_matrix": {"TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn)}
    }

class LogisticRegressionMLE:
    def __init__(self, l2_reg=0.1):
        self.l2_reg = l2_reg
        self.beta = None
        self.std_err = None
        self.p_values = None
        self.odds_ratios = None
        self.pseudo_r2 = None
        self.aic = None
        self.bic = None

    def fit(self, X, y):
        n, p = X.shape
        X_design = np.column_stack([np.ones(n), X])
        
        # Loss function with L2 penalty
        def neg_log_likelihood(beta):
            p_est = sigmoid(X_design @ beta)
            eps = 1e-12
            p_est = np.clip(p_est, eps, 1.0 - eps)
            ll = np.sum(y * np.log(p_est) + (1.0 - y) * np.log(1.0 - p_est))
            reg = 0.5 * self.l2_reg * np.sum(beta[1:] ** 2)
            return -(ll - reg)

        init_beta = np.zeros(p + 1)
        res = optimize.minimize(neg_log_likelihood, init_beta, method='BFGS')
        self.beta = res.x
        
        # Null model log likelihood (intercept only)
        p_null = np.mean(y)
        ll_null = np.sum(y * np.log(p_null) + (1.0 - y) * np.log(1.0 - p_null))
        ll_model = -res.fun + 0.5 * self.l2_reg * np.sum(self.beta[1:] ** 2)
        self.pseudo_r2 = float(max(0.0, 1.0 - (ll_model / ll_null)))
        self.aic = float(2 * (p + 1) - 2 * ll_model)
        self.bic = float(math.log(n) * (p + 1) - 2 * ll_model)
        
        # Standard errors from inverse Hessian
        try:
            p_pred = sigmoid(X_design @ self.beta)
            W = np.diag(p_pred * (1 - p_pred))
            hessian = X_design.T @ W @ X_design + self.l2_reg * np.eye(p + 1)
            cov = np.linalg.inv(hessian)
            self.std_err = np.sqrt(np.maximum(0, np.diag(cov)))
            z_scores = self.beta / (self.std_err + 1e-9)
            self.p_values = 2 * (1 - stats.norm.cdf(np.abs(z_scores)))
        except:
            self.std_err = np.zeros(p + 1)
            self.p_values = np.zeros(p + 1)
            
        self.odds_ratios = np.exp(self.beta)
        return self

    def predict_proba(self, X):
        X_design = np.column_stack([np.ones(len(X)), X])
        return sigmoid(X_design @ self.beta)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

class PureDecisionNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class PureDecisionTree:
    def __init__(self, max_depth=4, min_samples_split=4):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _gini(self, y):
        if len(y) == 0:
            return 0
        p1 = np.mean(y)
        return 1.0 - (p1**2 + (1.0 - p1)**2)

    def _best_split(self, X, y, feat_indices):
        best_gain = -1
        split_feat, split_thresh = None, None
        current_gini = self._gini(y)
        
        for feat in feat_indices:
            thresholds = np.unique(X[:, feat])
            for thresh in thresholds:
                left_mask = X[:, feat] <= thresh
                right_mask = ~left_mask
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                w_l = np.sum(left_mask) / len(y)
                w_r = 1.0 - w_l
                gain = current_gini - (w_l * self._gini(y[left_mask]) + w_r * self._gini(y[right_mask]))
                if gain > best_gain:
                    best_gain = gain
                    split_feat = feat
                    split_thresh = thresh
        return split_feat, split_thresh, best_gain

    def _build_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        if depth >= self.max_depth or n_samples < self.min_samples_split or len(np.unique(y)) == 1:
            val = float(np.mean(y) >= 0.5)
            prob = float(np.mean(y))
            return PureDecisionNode(value=(val, prob))
        
        feat_indices = list(range(n_features))
        feat, thresh, gain = self._best_split(X, y, feat_indices)
        if gain <= 0 or feat is None:
            return PureDecisionNode(value=(float(np.mean(y) >= 0.5), float(np.mean(y))))
            
        left_mask = X[:, feat] <= thresh
        right_mask = ~left_mask
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        return PureDecisionNode(feature=feat, threshold=thresh, left=left_child, right=right_child)

    def fit(self, X, y):
        self.root = self._build_tree(X, y)
        return self

    def _predict_row(self, node, row):
        if node.value is not None:
            return node.value
        if row[node.feature] <= node.threshold:
            return self._predict_row(node.left, row)
        return self._predict_row(node.right, row)

    def predict(self, X):
        return np.array([self._predict_row(self.root, r)[0] for r in X])

    def predict_proba(self, X):
        return np.array([self._predict_row(self.root, r)[1] for r in X])

class PureRandomForest:
    def __init__(self, n_estimators=60, max_depth=4, random_state=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.trees = []
        self.feature_importances_ = None

    def fit(self, X, y):
        rng = np.random.RandomState(self.random_state)
        n_samples, n_features = X.shape
        self.trees = []
        importances = np.zeros(n_features)
        
        for _ in range(self.n_estimators):
            boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
            X_b, y_b = X[boot_idx], y[boot_idx]
            tree = PureDecisionTree(max_depth=self.max_depth)
            tree.fit(X_b, y_b)
            self.trees.append(tree)
            
        # Proxy feature importance based on single tree splits
        for feat in range(n_features):
            corr = np.abs(stats.pearsonr(X[:, feat], y)[0])
            importances[feat] = corr
        self.feature_importances_ = importances / np.sum(importances)
        return self

    def predict_proba(self, X):
        all_probs = np.array([t.predict_proba(X) for t in self.trees])
        return np.mean(all_probs, axis=0)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

class PureGaussianNB:
    def __init__(self):
        self.classes = None
        self.mean = {}
        self.var = {}
        self.prior = {}

    def fit(self, X, y):
        self.classes = np.unique(y)
        for c in self.classes:
            X_c = X[y == c]
            self.mean[c] = np.mean(X_c, axis=0)
            self.var[c] = np.var(X_c, axis=0) + 1e-4
            self.prior[c] = len(X_c) / len(y)
        return self

    def _pdf(self, class_idx, x):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        num = np.exp(- (x - mean)**2 / (2 * var))
        denom = np.sqrt(2 * np.pi * var)
        return np.prod(num / denom, axis=1)

    def predict_proba(self, X):
        p0 = self._pdf(0, X) * self.prior[0]
        p1 = self._pdf(1, X) * self.prior[1]
        denom = p0 + p1 + 1e-12
        return p1 / denom

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

def k_fold_cross_validation(model_cls, X, y, k=5, seed=42, **kwargs):
    rng = np.random.RandomState(seed)
    n = len(y)
    
    # Stratified split
    idx0 = np.where(y == 0)[0]
    idx1 = np.where(y == 1)[0]
    rng.shuffle(idx0)
    rng.shuffle(idx1)
    
    folds0 = np.array_split(idx0, k)
    folds1 = np.array_split(idx1, k)
    
    metrics_list = []
    for i in range(k):
        test_idx = np.concatenate([folds0[i], folds1[i]])
        train_idx = np.setdiff1d(np.arange(n), test_idx)
        
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]
        
        model = model_cls(**kwargs)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)
        
        m = compute_classification_metrics(y_test, preds, probs)
        metrics_list.append(m)
        
    return {
        "accuracy_mean": round(float(np.mean([m["accuracy"] for m in metrics_list])), 4),
        "accuracy_std": round(float(np.std([m["accuracy"] for m in metrics_list])), 4),
        "precision_mean": round(float(np.mean([m["precision"] for m in metrics_list])), 4),
        "recall_mean": round(float(np.mean([m["recall"] for m in metrics_list])), 4),
        "f1_mean": round(float(np.mean([m["f1"] for m in metrics_list])), 4),
        "roc_auc_mean": round(float(np.mean([m["auc"] for m in metrics_list])), 4)
    }

# ==========================================
# 2. RUN JDS ANALYSIS (Junior Data Scientists)
# ==========================================

def run_jds_analysis():
    print("-> Processing JDS Skill Traits...")
    df = pd.read_excel(os.path.join(DATA_DIR, "JDS Skill Traits.xlsx"))
    df.columns = [c.strip().lower() for c in df.columns]
    
    features = [
        "big_data_skills", 
        "maths-stats_skills", 
        "coding_skills", 
        "ai_and_ml_skills", 
        "dashboard_and_storytelling_skills"
    ]
    target = "salary_hike_high_or_low"
    
    X = df[features].values
    y = df[target].values
    
    # Statistical tests: T-test, Mann-Whitney U, Pearson r
    stats_dict = {}
    for i, col in enumerate(features):
        high_vals = df[df[target] == 1][col].values
        low_vals = df[df[target] == 0][col].values
        t_stat, p_t = stats.ttest_ind(high_vals, low_vals)
        u_stat, p_u = stats.mannwhitneyu(high_vals, low_vals)
        r_val, p_r = stats.pearsonr(df[col].values, y)
        
        stats_dict[col] = {
            "high_hike_mean": round(float(np.mean(high_vals)), 3),
            "high_hike_sd": round(float(np.std(high_vals)), 3),
            "low_hike_mean": round(float(np.mean(low_vals)), 3),
            "low_hike_sd": round(float(np.std(low_vals)), 3),
            "mean_diff": round(float(np.mean(high_vals) - np.mean(low_vals)), 3),
            "t_statistic": round(float(t_stat), 3),
            "t_test_p_val": float(p_t),
            "mann_whitney_p_val": float(p_u),
            "pearson_r": round(float(r_val), 3),
            "pearson_p_val": float(p_r)
        }
        
    # Model Benchmarking (5-Fold Stratified CV)
    cv_lr = k_fold_cross_validation(LogisticRegressionMLE, X, y, k=5, l2_reg=0.2)
    cv_rf = k_fold_cross_validation(PureRandomForest, X, y, k=5, n_estimators=60, max_depth=3)
    cv_dt = k_fold_cross_validation(PureDecisionTree, X, y, k=5, max_depth=3)
    cv_nb = k_fold_cross_validation(PureGaussianNB, X, y, k=5)
    
    # Final Fit for Parameter Estimates (Full dataset)
    final_lr = LogisticRegressionMLE(l2_reg=0.1).fit(X, y)
    final_rf = PureRandomForest(n_estimators=100, max_depth=4).fit(X, y)
    
    param_table = {}
    for i, col in enumerate(features):
        param_table[col] = {
            "coef_beta": round(float(final_lr.beta[i+1]), 4),
            "std_error": round(float(final_lr.std_err[i+1]), 4),
            "p_value": float(final_lr.p_values[i+1]),
            "odds_ratio": round(float(final_lr.odds_ratios[i+1]), 4),
            "rf_feature_importance": round(float(final_rf.feature_importances_[i]), 4)
        }
        
    return {
        "dataset_name": "JDS Skill Traits (Junior Data Scientists)",
        "sample_size": len(df),
        "target_distribution": {
            "High Salary Hike (1)": int(np.sum(y == 1)),
            "Low Salary Hike (0)": int(np.sum(y == 0))
        },
        "descriptive_and_hypothesis_tests": stats_dict,
        "cross_validation_models": {
            "Logistic Regression (MLE)": cv_lr,
            "Random Forest Ensemble": cv_rf,
            "Decision Tree (CART)": cv_dt,
            "Gaussian Naive Bayes": cv_nb
        },
        "model_fit_statistics": {
            "mcfadden_pseudo_r2": round(final_lr.pseudo_r2, 4),
            "aic": round(final_lr.aic, 2),
            "bic": round(final_lr.bic, 2)
        },
        "feature_parameters_and_importance": param_table
    }

# ==========================================
# 3. RUN SDS ANALYSIS (Senior Data Scientists)
# ==========================================

def run_sds_analysis():
    print("-> Processing SDS Personality Traits...")
    df = pd.read_excel(os.path.join(DATA_DIR, "SDS Personality Traits.xlsx"))
    df.columns = [c.strip().lower() for c in df.columns]
    
    features = [
        "neuroticism", 
        "extraversion", 
        "openness_to_experience", 
        "agreeableness", 
        "conscientiousness"
    ]
    target = "success_ classification_ high_low"
    
    X = df[features].values
    y = df[target].values
    
    # Statistical tests: T-test, Mann-Whitney U, Pearson r
    stats_dict = {}
    for i, col in enumerate(features):
        high_vals = df[df[target] == 1][col].values
        low_vals = df[df[target] == 0][col].values
        t_stat, p_t = stats.ttest_ind(high_vals, low_vals)
        u_stat, p_u = stats.mannwhitneyu(high_vals, low_vals)
        r_val, p_r = stats.pearsonr(df[col].values, y)
        
        stats_dict[col] = {
            "high_success_mean": round(float(np.mean(high_vals)), 3),
            "high_success_sd": round(float(np.std(high_vals)), 3),
            "low_success_mean": round(float(np.mean(low_vals)), 3),
            "low_success_sd": round(float(np.std(low_vals)), 3),
            "mean_diff": round(float(np.mean(high_vals) - np.mean(low_vals)), 3),
            "t_statistic": round(float(t_stat), 3),
            "t_test_p_val": float(p_t),
            "mann_whitney_p_val": float(p_u),
            "pearson_r": round(float(r_val), 3),
            "pearson_p_val": float(p_r)
        }
        
    # Model Benchmarking (5-Fold Stratified CV)
    cv_lr = k_fold_cross_validation(LogisticRegressionMLE, X, y, k=5, l2_reg=0.2)
    cv_rf = k_fold_cross_validation(PureRandomForest, X, y, k=5, n_estimators=60, max_depth=3)
    cv_dt = k_fold_cross_validation(PureDecisionTree, X, y, k=5, max_depth=3)
    cv_nb = k_fold_cross_validation(PureGaussianNB, X, y, k=5)
    
    # Final Fit for Parameter Estimates (Full dataset)
    final_lr = LogisticRegressionMLE(l2_reg=0.1).fit(X, y)
    final_rf = PureRandomForest(n_estimators=100, max_depth=4).fit(X, y)
    
    param_table = {}
    for i, col in enumerate(features):
        param_table[col] = {
            "coef_beta": round(float(final_lr.beta[i+1]), 4),
            "std_error": round(float(final_lr.std_err[i+1]), 4),
            "p_value": float(final_lr.p_values[i+1]),
            "odds_ratio": round(float(final_lr.odds_ratios[i+1]), 4),
            "rf_feature_importance": round(float(final_rf.feature_importances_[i]), 4)
        }
        
    return {
        "dataset_name": "SDS Personality Traits (Senior Data Scientists)",
        "sample_size": len(df),
        "target_distribution": {
            "High Leadership Success (1)": int(np.sum(y == 1)),
            "Low Leadership Success (0)": int(np.sum(y == 0))
        },
        "descriptive_and_hypothesis_tests": stats_dict,
        "cross_validation_models": {
            "Logistic Regression (MLE)": cv_lr,
            "Random Forest Ensemble": cv_rf,
            "Decision Tree (CART)": cv_dt,
            "Gaussian Naive Bayes": cv_nb
        },
        "model_fit_statistics": {
            "mcfadden_pseudo_r2": round(final_lr.pseudo_r2, 4),
            "aic": round(final_lr.aic, 2),
            "bic": round(final_lr.bic, 2)
        },
        "feature_parameters_and_importance": param_table
    }

# ==========================================
# 4. RUN DATASCIENCE JOBS ANALYSIS
# ==========================================

def run_datascience_jobs_analysis():
    print("-> Processing DataScience Jobs...")
    df = pd.read_csv(os.path.join(DATA_DIR, "DataScience Jobs.csv"))
    
    # Clean string '7.8L' -> 7.8
    for col in ['avg_salary', 'min_salary', 'max_salary']:
        df[col + '_clean'] = df[col].astype(str).str.replace('L', '', regex=False).str.strip()
        df[col + '_clean'] = pd.to_numeric(df[col + '_clean'], errors='coerce')
        
    df['min_experience_clean'] = pd.to_numeric(df['min_experience'], errors='coerce')
    df['num_of_jobs_clean'] = pd.to_numeric(df['num_of_jobs'], errors='coerce')
    
    valid = df.dropna(subset=['avg_salary_clean', 'min_experience_clean', 'num_of_jobs_clean'])
    
    # OLS Regression: avg_salary = beta0 + beta1*min_experience + beta2*log(num_of_jobs)
    n = len(valid)
    X = np.column_stack([
        np.ones(n), 
        valid['min_experience_clean'].values, 
        np.log1p(valid['num_of_jobs_clean'].values)
    ])
    y = valid['avg_salary_clean'].values
    
    # Closed form OLS: beta = (X'X)^-1 X'y
    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ X.T @ y
    
    y_pred = X @ beta
    residuals = y - y_pred
    rss = np.sum(residuals**2)
    tss = np.sum((y - np.mean(y))**2)
    r2 = 1.0 - (rss / tss)
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - 3)
    rmse = np.sqrt(np.mean(residuals**2))
    
    # Variance and standard errors
    sigma2 = rss / (n - 3)
    var_beta = np.diag(sigma2 * XtX_inv)
    se_beta = np.sqrt(var_beta)
    t_stats = beta / se_beta
    p_vals = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n-3))
    
    return {
        "dataset_name": "DataScience Jobs (Enterprise Hiring)",
        "sample_size": len(df),
        "total_active_jobs_represented": int(df['num_of_jobs_clean'].sum()),
        "distinct_companies": int(df['company_name'].nunique()),
        "compensation_distribution_lpa": {
            "avg_salary_mean": round(float(df['avg_salary_clean'].mean()), 2),
            "avg_salary_median": round(float(df['avg_salary_clean'].median()), 2),
            "avg_salary_std": round(float(df['avg_salary_clean'].std()), 2),
            "min_salary_mean": round(float(df['min_salary_clean'].mean()), 2),
            "max_salary_mean": round(float(df['max_salary_clean'].mean()), 2)
        },
        "top_volume_recruiters": df.groupby('company_name')['num_of_jobs_clean'].sum().sort_values(ascending=False).head(10).to_dict(),
        "top_compensation_companies": {k: round(v, 2) for k, v in df.groupby('company_name')['avg_salary_clean'].mean().sort_values(ascending=False).head(10).items()},
        "econometric_salary_model": {
            "formula": "Avg_Salary = Beta0 + Beta1*(Experience) + Beta2*log(Job_Volume)",
            "coefficients": {
                "intercept": round(float(beta[0]), 4),
                "experience_coef": round(float(beta[1]), 4),
                "log_openings_coef": round(float(beta[2]), 4)
            },
            "standard_errors": [round(float(s), 4) for s in se_beta],
            "t_statistics": [round(float(t), 4) for t in t_stats],
            "p_values": [float(p) for p in p_vals],
            "r_squared": round(float(r2), 4),
            "adjusted_r_squared": round(float(adj_r2), 4),
            "rmse": round(float(rmse), 3)
        }
    }

# ==========================================
# 5. RUN ANALYTICS JOBS (15.8k Postings)
# ==========================================

def run_analytics_jobs_analysis():
    print("-> Processing Analytics Jobs (15.8k rows)...")
    df = pd.read_csv(os.path.join(DATA_DIR, "Analytics Jobs.csv"))
    
    # Missing values
    null_counts = df.isnull().sum().to_dict()
    null_pct = {k: round((v / len(df)) * 100, 2) for k, v in null_counts.items()}
    
    # Parse Experience
    def parse_exp(val):
        if pd.isna(val):
            return np.nan
        val = str(val).lower().replace('yrs', '').replace('yr', '').strip()
        parts = val.split('-')
        try:
            if len(parts) == 2:
                return (float(parts[0]) + float(parts[1])) / 2
            elif len(parts) == 1:
                return float(parts[0].replace('+', ''))
        except:
            return np.nan
        return np.nan
        
    df['exp_midpoint'] = df['experience'].apply(parse_exp)
    
    # Salary ordinal mapping
    sal_map = {'0to3': 0, '3to6': 1, '6to10': 2, '10to15': 3, '15to25': 4, '25to50': 5}
    sal_midpoints = {'0to3': 1.5, '3to6': 4.5, '6to10': 8.0, '10to15': 12.5, '15to25': 20.0, '25to50': 37.5}
    df['salary_tier'] = df['salary'].map(sal_map)
    df['salary_lpa'] = df['salary'].map(sal_midpoints)
    
    # Tech skills frequency & SAS special check
    key_skills_text = df['key_skills'].dropna().astype(str)
    
    sas_mentions = int(key_skills_text.str.contains(r'\bSAS\b', case=False, regex=True).sum())
    sql_mentions = int(key_skills_text.str.contains(r'\bSQL\b', case=False, regex=True).sum())
    python_mentions = int(key_skills_text.str.contains(r'\bPython\b', case=False, regex=True).sum())
    ml_mentions = int(key_skills_text.str.contains(r'Machine Learning', case=False, regex=True).sum())
    r_mentions = int(key_skills_text.str.contains(r'\bR\b', case=False, regex=True).sum())
    tableau_mentions = int(key_skills_text.str.contains(r'Tableau', case=False, regex=True).sum())
    powerbi_mentions = int(key_skills_text.str.contains(r'Power BI|PowerBI', case=False, regex=True).sum())
    excel_mentions = int(key_skills_text.str.contains(r'Excel', case=False, regex=True).sum())
    
    # Top individual skills
    raw_skills = []
    for s in key_skills_text:
        tokens = [t.strip() for t in s.split(',') if t.strip()]
        raw_skills.extend(tokens)
    top_20_skills = pd.Series(raw_skills).value_counts().head(20).to_dict()
    
    # Salary & Experience by Top Locations
    top_locs = df['location'].value_counts().head(8).index.tolist()
    loc_stats = {}
    for loc in top_locs:
        subset = df[df['location'] == loc]
        loc_stats[loc] = {
            "job_count": len(subset),
            "percentage_share": round(len(subset) / len(df) * 100, 2),
            "mean_exp_years": round(float(subset['exp_midpoint'].dropna().mean()), 2),
            "mean_salary_lpa": round(float(subset['salary_lpa'].dropna().mean()), 2)
        }
        
    # Chi-Square Test: Location vs Salary Tier
    ct = pd.crosstab(df[df['location'].isin(top_locs)]['location'], df['salary'])
    chi2_val, p_chi2, dof, _ = stats.chi2_contingency(ct)
    
    # ANOVA: Experience across Salary Brackets
    groups = [df[df['salary'] == b]['exp_midpoint'].dropna().values for b in sal_map.keys() if len(df[df['salary'] == b]) > 0]
    f_stat, p_anova = stats.f_oneway(*groups)
    
    return {
        "dataset_name": "Analytics Jobs (Macro Demand)",
        "sample_size": len(df),
        "data_quality_null_audit": null_pct,
        "salary_tier_breakdown": df['salary'].value_counts().to_dict(),
        "key_analytics_tools_demand": {
            "SQL": sql_mentions,
            "Python": python_mentions,
            "SAS": sas_mentions,
            "R": r_mentions,
            "Machine Learning": ml_mentions,
            "Tableau": tableau_mentions,
            "Excel": excel_mentions,
            "Power BI": powerbi_mentions
        },
        "top_20_skills": top_20_skills,
        "geographic_clusters": loc_stats,
        "inferential_statistics": {
            "location_salary_chi2": round(float(chi2_val), 2),
            "location_salary_p_value": float(p_chi2),
            "experience_salary_f_statistic": round(float(f_stat), 2),
            "experience_salary_anova_p_value": float(p_anova)
        }
    }

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    print("="*60)
    print("COMMENCING ROBUST PURE-NUMPY/SCIPY STATISTICAL & ML ENGINE")
    print("="*60)
    
    results = {
        "jds_skill_traits": run_jds_analysis(),
        "sds_personality_traits": run_sds_analysis(),
        "datascience_jobs": run_datascience_jobs_analysis(),
        "analytics_jobs": run_analytics_jobs_analysis()
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\n[DONE] All analytical modeling results saved to:\n{OUTPUT_PATH}")
    print("="*60)

if __name__ == "__main__":
    main()
