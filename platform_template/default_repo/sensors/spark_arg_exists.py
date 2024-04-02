if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def spark_arg_exists(*args, **kwargs) -> bool:
    if (spark := kwargs.get("spark")) is not None:
        print('kwargs["spark"] variable exists')
        print(f"{spark=}")
        print(f"{spark.sparkContext.uiWebUrl=}")

    return spark is not None
