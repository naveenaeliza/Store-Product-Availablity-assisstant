import streamlit as st
import requests

# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000/api/availability"

# ============================================================
# USER LOCATION
# Paste your fixed coordinates here
# ============================================================

USER_LATITUDE = 10.0099536
USER_LONGITUDE = 76.364782
# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Store Availability Checker",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 Store Availability Checker")

st.caption(
    f"Current Location: ({USER_LATITUDE}, {USER_LONGITUDE})"
)

st.divider()

query = st.text_input(
    "Search",
    placeholder="Example: iPhone 12 store available near me"
)

search = st.button(
    "Search",
    use_container_width=True
)

# ============================================================
# SEARCH
# ============================================================

if search:

    if not query.strip():

        st.warning("Please enter a product query.")

    else:

        payload = {
            "query": query,
            "user_latitude": USER_LATITUDE,
            "user_longitude": USER_LONGITUDE
        }

        try:

            with st.spinner("Searching nearby stores..."):

                response = requests.post(
                    BACKEND_URL,
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:

                data = response.json()

                st.success("Search Completed")

                st.subheader("Result")

                # If your backend returns:
                # {
                #   "response": "...."
                # }

                if "response" in data:
                    st.write(data["response"])

                else:
                    st.json(data)

            else:

                st.error(
                    f"Backend Error ({response.status_code})"
                )

                st.code(response.text)

        except Exception as e:

            st.error(str(e))