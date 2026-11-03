from datetime import date

from rest_framework import serializers


MIN_PRODUCT_CREATOR_AGE = 18


def calculate_age(birthdate: date, today: date | None = None) -> int:
    """Return a person's full age, taking month and day into account."""
    today = today or date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )


def validate_product_creator_age(request, minimum_age: int = MIN_PRODUCT_CREATOR_AGE) -> None:
    """Validate age using the signed ``birthdate`` claim from the access token."""
    token = getattr(request, "auth", None)
    raw_birthdate = token.get("birthdate") if token is not None else None

    if not raw_birthdate:
        raise serializers.ValidationError(
            {"birthdate": "Укажите дату рождения, чтобы создать продукт."}
        )

    try:
        birthdate = date.fromisoformat(raw_birthdate)
    except (TypeError, ValueError):
        raise serializers.ValidationError(
            {"birthdate": "В JWT-токене указана некорректная дата рождения."}
        )

    if birthdate > date.today():
        raise serializers.ValidationError(
            {"birthdate": "Дата рождения не может быть в будущем."}
        )

    if calculate_age(birthdate) < minimum_age:
        raise serializers.ValidationError(
            {
                "birthdate": (
                    f"Вам должно быть {minimum_age} лет, чтобы создать продукт."
                )
            }
        )
