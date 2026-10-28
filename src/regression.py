from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


class RegressionPipeline:
    """
    End-to-end regression modeling for customer purchase amount prediction.
    Strictly prevents target leakage by fitting transformers exclusively on the training set.
    """

    CATEGORICAL_FEATURES = [
        "gender", "category", "season", "subscription_status",
        "shipping_type", "discount_applied", "payment_method", "age_group"
    ]

    NUMERIC_FEATURES = [
        "age", "review_rating", "previous_purchases", "purchase_frequency_days"
    ]

    def __init__(self, df: pd.DataFrame, target_col: str = "purchase_amount", test_size: float = 0.2, random_state: int = 42):
        self.df = df.copy()
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.preprocessor = None
        self.model = None
        self.feature_names = []

    def prepare_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Isolate features and target, then split train/test sets."""
        feature_cols = [c for c in self.CATEGORICAL_FEATURES + self.NUMERIC_FEATURES if c in self.df.columns]
        X = self.df[feature_cols]
        y = self.df[self.target_col]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def build_transformer(self) -> ColumnTransformer:
        """Construct ColumnTransformer for one-hot encoding categoricals and scaling numerics."""
        available_cat = [c for c in self.CATEGORICAL_FEATURES if c in self.X_train.columns]
        available_num = [c for c in self.NUMERIC_FEATURES if c in self.X_train.columns]

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), available_num),
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), available_cat)
            ]
        )
        return self.preprocessor

    def train(self, model_type: str = "linear", alpha: float = 1.0) -> dict:
        """Fit preprocessor and regression model on training data, then evaluate on test data."""
        if self.X_train is None:
            self.prepare_data()

        self.build_transformer()

        # Fit preprocessor strictly on training data
        X_train_proc = self.preprocessor.fit_transform(self.X_train)
        X_test_proc = self.preprocessor.transform(self.X_test)

        # Retrieve transformed feature names
        num_names = self.preprocessor.transformers_[0][2]
        cat_encoder = self.preprocessor.transformers_[1][1]
        cat_names = list(cat_encoder.get_feature_names_out(self.preprocessor.transformers_[1][2]))
        self.feature_names = list(num_names) + cat_names

        # Baseline: Predict mean of y_train
        y_train_mean = self.y_train.mean()
        y_pred_baseline = np.full_like(self.y_test, fill_value=y_train_mean)
        baseline_mae = mean_absolute_error(self.y_test, y_pred_baseline)
        baseline_rmse = root_mean_squared_error(self.y_test, y_pred_baseline)
        baseline_r2 = r2_score(self.y_test, y_pred_baseline)

        # Fit chosen model
        if model_type == "ridge":
            self.model = Ridge(alpha=alpha, random_state=self.random_state)
        else:
            self.model = LinearRegression()

        self.model.fit(X_train_proc, self.y_train)

        # Predictions
        y_pred_train = self.model.predict(X_train_proc)
        y_pred_test = self.model.predict(X_test_proc)

        # Metrics
        train_mae = mean_absolute_error(self.y_train, y_pred_train)
        train_rmse = root_mean_squared_error(self.y_train, y_pred_train)
        train_r2 = r2_score(self.y_train, y_pred_train)

        test_mae = mean_absolute_error(self.y_test, y_pred_test)
        test_rmse = root_mean_squared_error(self.y_test, y_pred_test)
        test_r2 = r2_score(self.y_test, y_pred_test)

        # Extract coefficients
        coef_df = pd.DataFrame({
            "feature": self.feature_names,
            "coefficient": self.model.coef_
        }).sort_values(by="coefficient", key=abs, ascending=False)

        results = {
            "model_type": model_type,
            "baseline": {
                "mae": float(baseline_mae),
                "rmse": float(baseline_rmse),
                "r2": float(baseline_r2)
            },
            "train_metrics": {
                "mae": float(train_mae),
                "rmse": float(train_rmse),
                "r2": float(train_r2)
            },
            "test_metrics": {
                "mae": float(test_mae),
                "rmse": float(test_rmse),
                "r2": float(test_r2)
            },
            "intercept": float(self.model.intercept_),
            "coefficients": coef_df,
            "predictions": {
                "y_test": self.y_test.values,
                "y_pred": y_pred_test,
                "residuals": self.y_test.values - y_pred_test
            },
            "limitations": (
                "Synthetic customer shopping datasets feature predominantly uniform distributions across "
                "purchase amounts and weak bivariate linear relationships with demographic features. "
                "Consequently, linear models achieve R² values near 0, demonstrating that purchase amounts "
                "in this dataset cannot be reliably predicted from demographic attributes alone."
            )
        }
        return results
