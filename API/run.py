from app import run_api

if __name__ == '__main__':
    run_api(debug=True, path_to_config="config_app.yaml", path_to_algo_config="config_algo.yaml")
