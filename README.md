# Python Executor


## Build the Docker image
> docker build -t python-executor .

## Run the Docker container locally
> docker run -p 9090:8080 python-executor

## Test the API locally
> curl -X POST http://localhost:9090/execute -H "Content-Type: application/json" -d '{"script": "def main():\n    return {\"msg\": \"hello\"}\n\nif __name__ == \"__main__\":\n    import json\n    print(json.dumps(main()))"}'

## Google Cloud Run service URL
https://python-executor-53465707225.us-central1.run.app/execute

# Testing using Google service URL

## Success Case: Arithmetic Script
> curl -X POST https://python-executor-53465707225.us-central1.run.app/execute -H "Content-Type: application/json" -d '{"script": "def main():\n    a = 15\n    b = 7\n    return {\"sum\": a + b, \"product\": a * b, \"difference\": a - b, \"quotient\": a / b}\n\nif __name__ == \"__main__\":\n    import json\n    print(json.dumps(main()))"}'

## Missing main() Function
> curl -X POST https://python-executor-53465707225.us-central1.run.app/execute -H "Content-Type: application/json" -d '{"script": "print(123)"}'

##  main() Returns Non-JSON
> curl -X POST https://python-executor-53465707225.us-central1.run.app/execute -H "Content-Type: application/json" -d '{"script": "def main():\n    return 123"}'

## Numpy Test
> curl -X POST https://python-executor-53465707225.us-central1.run.app/execute -H "Content-Type: application/json" -d '{"script": "import numpy as np\ndef main():\n    arr = np.array([1, 2, 3])\n    return {\"mean\": float(np.mean(arr))}\n\nif __name__ == \"__main__\":\n    import json\n    print(json.dumps(main()))"}'

## Pandas Test
> curl -X POST https://python-executor-53465707225.us-central1.run.app/execute -H "Content-Type: application/json" -d '{"script": "import pandas as pd\ndef main():\n    df = pd.DataFrame({\"a\": [1, 2, 3]})\n    return {\"sum\": int(df[\"a\"].sum())}\n\nif __name__ == \"__main__\":\n    import json\n    print(json.dumps(main()))"}'


# Time taken
It has taken more than 6 to 7 hrs to finish this. Though it is a simple task, most of the time has taken to debug and fix the nsjail config errors as there is no proper documentation for it. 
