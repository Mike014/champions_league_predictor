import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from flask import Flask, request, render_template, flash
import numpy as np

# Load the dataset
df_performance = pd.read_csv('Data/UCL_AllTime_Performance_Table.csv')

# Print column names for verification
print(df_performance.columns)

# Clean the 'goals' column in df_performance
df_performance['goals'] = df_performance['goals'].apply(lambda x: int(x.split(':')[0]))

# Prepare data for the model
X = df_performance[['M.', 'W', 'D', 'L', 'Dif', 'Pt.']]
y = df_performance['goals']  # Predict goals scored in a season

# Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Polynomial Features
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_scaled)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Create and train the model
model = Ridge(alpha=1.0)  # You can also try Lasso or other models
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Cross-Validation
cv_scores = cross_val_score(model, X_poly, y, cv=5, scoring='neg_mean_squared_error')
print("Cross-Validated MSE:", -cv_scores.mean())

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_goals = None
    error_message = None
    if request.method == 'POST':
        try:
            # Extract form data
            form_data = {key: request.form[key] for key in ['M', 'W', 'D', 'L', 'Dif', 'Pt']}

            # Ensure all fields are filled
            if all(form_data.values()):
                # Convert form data to float
                form_data = {key: float(value) for key, value in form_data.items()}

                # Normalize input data
                input_data = scaler.transform(np.array([[form_data['M'], form_data['W'], form_data['D'], form_data['L'], form_data['Dif'], form_data['Pt']]]))
                input_data_poly = poly.transform(input_data)
                print(f"Normalized Input Data: {input_data_poly}")
                predicted_goals = model.predict(input_data_poly)[0]
                predicted_goals = round(predicted_goals)

                # Print user input and result
                print(f"User Input: {form_data}")
                print(f"Predicted Goals: {predicted_goals}")
            else:
                error_message = "Please ensure all fields are filled out correctly with numeric values."
                flash(error_message)
        except ValueError:
            error_message = "Please ensure all fields are filled out correctly with numeric values."
            flash(error_message)

    return render_template('index.html', predicted_goals=predicted_goals, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)