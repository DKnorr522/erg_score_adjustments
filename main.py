import streamlit as st


def seconds_to_time_formatted(seconds):
    minutes = int(seconds / 60)
    seconds = round(seconds % 60, 2)
    time_formatted = f"{minutes}:{seconds.zfill(2)}"
    return time_formatted


def main():
    st.header(
        "Age and weight adjustments for erg scores"
    )

    piece_distance = 500  # meters

    col_question, col_distance = st.columns(2)

    with col_question:
        time_type = st.radio(
            label="Total time or split",
            options=[
                "Split",
                "Time"
            ]
        )
    if time_type == "Time":
        with col_distance:
            piece_distance = st.number_input(
                label="Piece Distance",
                min_value=500,
                max_value=10000,
                value=1000,
                step=500
            )

    max_minutes = {
        "Split": 5,
        "Time": 100
    }

    col_min, col_sec = st.columns(2)

    with col_min:
        minutes = st.number_input(
            label="Minutes",
            min_value=0,
            max_value=max_minutes[time_type],
            value=2,
            step=1
        )
    with col_sec:
        seconds = round(
            st.number_input(
                label="Seconds",
                min_value=0.0,
                max_value=59.9,
                value=30.0,
                step=0.1,
                format="%.1f"
            ),
            1
        )

    total_seconds = minutes * 60 + seconds

    col_age, col_weight = st.columns(2)

    adjustment_weight, adjustment_age = 1, 0
    with col_age:
        adjust_age = st.checkbox(
            label="Age adjust",
            value=False
        )
        if adjust_age:
            try:
                age = int(
                    st.text_input(
                        label="Age as of December 31 of the year of the test",
                        value=""
                    )
                )
                distance_factor = piece_distance / 1000
                age = 27 if age < 27 else age
                adjustment_age = distance_factor * (((age - 27) ** 2) * 0.02)

            except ValueError:
                st.write("Please enter an integer")

    with col_weight:
        adjust_weight = st.checkbox(
            label="Weight adjust",
            value=False
        )
        if adjust_weight:
            try:
                weight = float(
                    st.text_input(
                        label="Weight at time of test",
                        value=""
                    )
                )
                adjustment_weight = (weight / 270) ** 0.222
            except ValueError:
                st.write("Please enter a number")

    total_seconds_adjusted = round(
        total_seconds * adjustment_weight - adjustment_age,
        1
    )
    total_time_adjusted_formatted = seconds_to_time_formatted(
        total_seconds_adjusted
    )
    st.subheader(f"Final {time_type}: {total_time_adjusted_formatted}")


if __name__ == '__main__':
    main()
