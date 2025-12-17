#metro ticket booking app

import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image
from gtts import gTTS
import base64

#QR GENERATION FUNCTION

def generate_qr(data):
    qr = qrcode.QRCode(version=1,box_size=10,border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black",back_color="white")
    return img

#STREAMLIT UI
#st.title("metro Ticket BOOKING")
stations = ["Ameerpet","Miyapur","LB Nager","KPHB","JNTU"]
name = st.text_input("passenger name")
source = st.selectbox("source station",stations)
destination = st.selectbox("destination station",stations)
no_tickets = st.number_input("number of tickets",min_value=1,value=1)
price_per_ticket=30
total_amount= no_tickets*price_per_ticket
st.info(f"total amount:{total_amount}")

#BOOKING BUTTON

if st.button("book ticket"):

    if name.strip() =="":
        st.error("plese enter passengerf name.")


    elif source == destination:
        st.error("source and destination cannot be the same")

    else:
        #generate booking id
        booking_id = str(uuid.uuid4()) [:8]
        #QR CODE GENERATION
        qr_data =(
            f"BookingID: {booking_id}\n"
            f"Name: {name}\nfrom: {source}\nTo: {destination}\nTickets:{no_tickets}"
            )
        qr_img = generate_qr(qr_data)

        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        st.success("Ticket booked successfully")

        st.write("### ticket details")
        st.write(f"booking ID: {booking_id}")
        st.write(f"passenger:{ name}")
        st.write(f"from:{source}")
        st.write(f"to:{destination}")
        st.write(f"tickets:{no_tickets}")
        st.write(f"amount paid:{total_amount}")
        st.image(qr_bytes,width=200)
