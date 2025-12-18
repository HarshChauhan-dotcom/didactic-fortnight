import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image

# --qr generation function--
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# --streamlit ui--
st.set_page_config(page_title="Metro Ticket Booking")
st.title("🚇 Metro Ticket Booking System with QR")

stations = ["Ameerpet", "KPHB", "JNTU", "Balanagar", "Jubilee Hills"]

# Inputs
name = st.text_input("Passenger Name")
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("Source Station", stations)
with col2:
    destination = st.selectbox("Destination Station", stations)

no_tickets = st.number_input("No. of Tickets", min_value=1, value=1)

# Cab requirement section
st.write("---")
st.write("### 🚕 Cab Services")
need_cab = st.radio("Do you need a cab?", ["No", "Yes"], horizontal=True)

drop_location = ""
if need_cab == "Yes":
    drop_location = st.text_input("Enter Drop Location")

# Price calculation
price_per_ticket = 30
total_amount = no_tickets * price_per_ticket
st.info(f"Total Amount: ₹{total_amount}")

# --booking button--
if st.button("Book Ticket"):
    if not name:
        st.error("Please enter passenger name")
    elif source == destination:
        st.error("Source and destination can't be same")
    elif need_cab == "Yes" and not drop_location:
        st.error("Please enter drop location for the cab")
    else:
        booking_id = str(uuid.uuid4())[:8]

        # --qr code generator--
        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Cab Required: {need_cab}\n"
            f"Drop: {drop_location if drop_location else 'N/A'}"
        )
        
        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        # Success Output
        st.success("Ticket Booked Successfully!")
        
        st.write(f"**Booking ID**: {booking_id}")
        st.write(f"**Passenger Name**: {name}")
        st.write(f"**Journey**: {source} to {destination}")
        st.write(f"**Tickets**: {no_tickets}")
        st.write(f"**Cab Service**: {need_cab}")
        if need_cab == "Yes":
            st.write(f"**Drop Location**: {drop_location}")
        st.write(f"**Amount Paid**: ₹{total_amount}")
        
        st.image(qr_bytes, caption="Scan this at the entry gate", width=250)
