#metro ticket booking app

import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image
import base64
#--qr generation function--
def generate_qr(data):
    qr=qrcode.QRCode(version=1,box_size=10,border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black",back_color="white")
    return img

#--streamlit ui--

st.set_page_config(page_title="metro ticket booking")
st.title("metro ticket booking system with qr+auto voice")
stations=["ameerpet","kphb","jntu","balanagar","jubliee hills"]
name=st.text_input("passenger name")
source=st.selectbox("source station",stations)
destination=st.selectbox("destination station",stations)
no_tickets=st.number_input("no.of tickets",min_value=1,value=1)
price_per_ticket=30
total_amount=no_tickets*price_per_ticket
st.info(f"total amount:(total_amount)")

#--booking button--

if st.button("book ticket"):
    st.error("please enter passenger name")
elif source==destination:
    st.error("source and destination cant be same")
else:
    booking_id=str(uuid.uuid4())[:8]

    #--qr code generator--

    qr_data=(f"bookingid:(booking_id)\n"f"name:{name}\nfrom:{source}\nTo:{destination}\n tickets:{no_tickets}")
    qr_img=generate_qr(qr_data)
    buf=BytesIO()
    qr_img.save(buf,format="PNG")
    qr_bytes=buf.getvalue()
    st.success("ticket booked successfully.")
    st.write(f"**booking id**:{booking_id}")
    st.write(f"**passenger name**:{name}")
    st.write(f"**from**:{source}")
    st.write(f"**to**:{destination}")
    st.write(f"**tickets**:{no_tickets}")
    st.write(f"**amount paid**:{total_amount}")
    st.image(qr_bytes,width=250)

