import pandas as pd


def main() -> None:
    df = pd.read_csv("data.csv")
    df["temperature_F"] = df["temperature"] * 1.8 + 32
    print(df.to_string(index=False))
    df.to_csv("/tmp/output.csv", index=False)


if __name__ == "__main__":
    main()
