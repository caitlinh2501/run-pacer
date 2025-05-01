import json
import argparse

def load_runs(filename):
    with open(filename) as f:
        return json.load(f)

def calculate_pace_km(time_min, distance_km):
    return time_min / distance_km

def predict_pace_for_distance(recent_runs, target_distance_km):
    paces = [calculate_pace_km(run['time_min'], run['distance_km']) for run in recent_runs]
    avg_pace = sum(paces) / len(paces)

    easy_runs = all(run['effort'] <= 5 for run in recent_runs)
    if easy_runs:
        predicted_pace = avg_pace * 0.97
    else:
        predicted_pace = avg_pace

    predicted_time = predicted_pace * target_distance_km
    return round(predicted_pace, 2), predicted_time

def minutes_to_hms(minutes_float):
    total_seconds = int(minutes_float * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict your running pace for a given distance.")
    parser.add_argument('--distance', type=float, default=10.0, help='Target distance in km (e.g., 5, 10, 21.1, 42.2)')
    args = parser.parse_args()

    runs = load_runs('run_data.json')
    pace, time_min = predict_pace_for_distance(runs, args.distance)
    time_formatted = minutes_to_hms(time_min)

    print(f"Predicted pace for {args.distance} km: {pace} min/km")
    print(f"Estimated finish time: {time_formatted} (hh:mm:ss)")
