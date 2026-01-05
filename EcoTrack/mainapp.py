from flask import Flask, render_template, request
import os

# cross-platform paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, 'templates')
static_path = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)

# simple fallback co2 data
def get_co2_data():
    return 19.6, 4.5  # uae, world (tons per capita)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/charts")
def charts():
    plastic = request.args.get('plastic', 0, type=int)
    food = request.args.get('food', 0, type=int)
    clothes = request.args.get('clothes', 0, type=int)
    electricity = request.args.get('electricity', 0, type=int)
    water = request.args.get('water', 0, type=int)
    flights = request.args.get('flights', 0, type=int)
    transport = request.args.get('transport', 'car')

    labels = ["Plastic", "Food", "Clothes", "Electricity", "Water", "Transport"]

    plastic_co2 = plastic * 0.01
    food_co2 = food * 0.002
    clothes_co2 = clothes * 0.04
    electricity_co2 = electricity * 0.0007
    water_co2 = water * 0.003
    flights_co2 = flights * 0.25

    transport_total = 0.17 if transport == "car" else 0.07 if transport == "public" else 0
    transport_total += flights_co2

    values = [plastic_co2, food_co2, clothes_co2, electricity_co2, water_co2, transport_total]

    uae_avg_tons, world_avg_tons = get_co2_data()

    personal_total_kg = round(sum(values) * 1000, 1)

    visual_country_kg = round(personal_total_kg * 1.1, 1)
    visual_global_kg = round(personal_total_kg * 0.9, 1)

    return render_template(
        "charts.html",
        labels=labels,
        values=values,
        country_avg=visual_country_kg,
        global_avg=visual_global_kg
    )

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/result', methods=['POST'])
def result():
    plastic = int(request.form.get('plastic', 0))
    food = int(request.form.get('food', 0))
    clothes = int(request.form.get('clothes', 0))
    electricity = int(request.form.get('electricity', 0))
    transport = request.form.get('transport', 'car')
    water = int(request.form.get('water', 0))
    flights = int(request.form.get('flights', 0))
    diet = request.form.get('diet', 'mixed')
    recycling = request.form.get('recycling', 'sometimes')

    score = 100
    score -= plastic * 1
    score -= food * 1.5
    score -= clothes * 2
    score -= electricity / 200
    score -= water / 5
    score -= flights * 3
    score += 5 if diet == 'veg' else -3 if diet == 'meat' else 0
    score += 5 if recycling == 'always' else -3 if recycling == 'rarely' else 0
    score += 5 if transport == 'cycle' else -8 if transport == 'car' else -3 if transport == 'public' else 0
    score = max(0, min(100, score))

    total_co2 = (
        plastic * 0.01 +
        food * 0.002 +
        clothes * 0.04 +
        electricity * 0.0007 +
        water * 0.003 +
        flights * 0.25 +
        (0.17 if transport == 'car' else 0.07 if transport == 'public' else 0)
    )
    total_co2_kg = total_co2 * 1000

    tips = []
    if plastic > 5: tips.append("Switch to a reusable water bottle to cut down on your plastic usage.")
    if food > 2: tips.append("Try planning your meals to reduce food waste.")
    if clothes > 3: tips.append("Reducing your clothing purchases would save a lot of water and energy.")
    if electricity > 200: tips.append('Turn off appliances when not in use to save electricity.')
    if water > 8: tips.append("Shorter showers (1-2 minutes less) would save water & energy.")
    if flights > 0: tips.append("Consider fewer flights for long trips.")
    if diet == 'meat': tips.append("Reducing red meat intake can significantly lower your footprint.")
    if recycling == 'rarely': tips.append("Start sorting your recyclables to reduce the amount of landfill waste you produce.")

    data = {
        "plastic": plastic,
        "food": food,
        "clothes": clothes,
        "electricity": electricity,
        "water": water,
        "flights": flights,
        "transport": transport,
        "diet": diet,
        "recycling": recycling
    }

    return render_template('result.html', score=score, tips=tips, data=data, total_co2=round(total_co2_kg, 1))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
