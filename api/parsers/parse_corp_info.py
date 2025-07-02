def parse_corp_info(html_content: str) -> dict:
    """
    从新浪财经公司信息HTML中提取关键信息
    :param html_content: 包含公司信息的HTML内容
    :return: 包含公司信息的字典
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")
    info_dict = {}
    table = soup.find("table", id="comInfo1")

    if not table:
        return info_dict

    # 提取基本信息
    info_dict["company_name"] = (
        table.find("td", string="公司名称：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["english_name"] = (
        table.find("td", string="公司英文名称：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["listing_date"] = (
        table.find("td", string="上市日期：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["establish_date"] = (
        table.find("td", string="成立日期：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["registered_capital"] = (
        table.find("td", string="注册资本：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )

    # 提取地址信息
    info_dict["registered_address"] = (
        table.find("td", string="注册地址：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["office_address"] = (
        table.find("td", string="办公地址：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )

    # 提取公司简介和主营业务
    info_dict["company_profile"] = (
        table.find("td", string="公司简介：")
        .find_next_sibling("td")
        .get_text(strip=True)
        .replace("&nbsp;", " ")
    )
    info_dict["main_business"] = (
        table.find("td", string="主营业务：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )

    # 提取联系方式
    info_dict["phone"] = (
        table.find("td", string="公司电话：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["email"] = (
        table.find("td", string="公司电子邮箱：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    info_dict["website"] = (
        table.find("td", string="公司网址：")
        .find_next_sibling("td")
        .get_text(strip=True)
    )

    # 提取更名历史
    name_history = []
    name_td = table.find("td", string="证券简称更名历史：")
    if name_td:
        name_history = [
            name.strip()
            for name in name_td.find_next_sibling("td").get_text(strip=True).split(";")
            if name.strip()
        ]
    info_dict["name_history"] = name_history

    return info_dict