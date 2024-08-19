# 导入requests库
import httpx
import xml.dom.minidom

def login(username, password, baseURL="https://pass.sdu.edu.cn/") -> str:
# 发送第一个请求，获取ticket
    ticket = httpx.post(
        f"{baseURL}cas/restlet/tickets",
        data={"username": username, "password": password, "lt": "LT-1-1-1"},
    ).text

    # 检查ticket是否以TGT开头
    if not ticket.startswith("TGT"):
        raise Exception("ticket should start with TGT. Check your username and password.")

    # 发送第二个请求，获取sTicket
    sTicket = httpx.post(f"{baseURL}cas/restlet/tickets/{ticket}",content="service=https://service.sdu.edu.cn/tp_up/view?m=up", headers={"Content-Type": "text/plain"}).text

    # 检查sTicket是否以ST开头
    if not sTicket.startswith("ST"):
        raise Exception("sTicket should start with ST")

    return sTicket

def get_user_name_and_id(sTicket, baseURL="https://pass.sdu.edu.cn/"):
    user_data = xml.dom.minidom.parseString(httpx.get(
        f"{baseURL}cas/serviceValidate",
        params={
            "ticket": sTicket,
            "service": "https://service.sdu.edu.cn/tp_up/view?m=up",
        },
    ).text)
    name = user_data.getElementsByTagName("cas:USER_NAME")[0].childNodes[0].data
    student_id = user_data.getElementsByTagName("sso:user")[0].childNodes[0].data
    return name, student_id
