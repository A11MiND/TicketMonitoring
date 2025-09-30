import json
import logging

import requests
from requests import Response

from Monitor import Monitor


class UUTIX(Monitor):

    token = str()

    def __init__(self, perform: dict) -> None:
        super().__init__()
        file = open("config.json", "r", encoding="utf-8")
        config = json.load(file)
        self.token = config.get("token", {}).get("uutix", "")
        file.close()
        
        self.performId = perform.get('show_id')
        self.show_info = {
            "platform": "UUTIX",
            "seat_info": list(),
            "session_info": list(),
            "show_id": perform.get('show_id'),
            "show_name": perform.get('show_name')
        }
        logging.info(f"UUTIX {perform.get('show_name')} 开始加载")
        self.get_show_infos()
        logging.info(f"UUTIX {self.show_info.get('show_name')} 加载成功")

    def get_show_infos(self):
        show_id = self.show_info.get('show_id')
        
        # 获取当前时间戳
        import time
        timestamp = str(int(time.time() * 1000))
        
        # 使用从HAR文件中发现的真实API端点
        # 1. 获取项目基础信息
        base_url = f"https://www.uutix.com/api/oversea/project/base?t={timestamp}&projectId={show_id}&source=1&WuKongReady=h5"
        
        response = self.request(base_url)
        
        # 检查HTTP状态码
        if response.status_code == 801:
            # 处理验证码挑战
            try:
                error_data = response.json()
                verify_url = error_data.get("customData", {}).get("verifyUrl", "")
                logging.error("UUTIX触发了反爬虫验证码挑战")
                logging.error(f"验证URL: {verify_url}")
                logging.error("解决方案:")
                logging.error("1. 在浏览器中访问UUTIX网站完成验证码")
                logging.error("2. 获取验证后的新Cookie")
                logging.error("3. 更新Monitor_UUTIX.py中的Cookie")
                raise Exception("UUTIX需要验证码验证，请在浏览器中完成验证")
            except:
                logging.error("UUTIX返回验证码挑战但解析失败")
                raise Exception("UUTIX验证码挑战")
        elif response.status_code != 200:
            logging.error(f"UUTIX项目基础信息API请求失败: HTTP {response.status_code}")
            logging.error(f"响应内容: {response.text[:200]}")
            raise Exception(f"UUTIX项目基础信息API请求失败: HTTP {response.status_code}")
        
        try:
            base_data = response.json()
            logging.info(f"UUTIX项目基础信息响应: {base_data}")
        except:
            logging.error("UUTIX项目基础信息API返回非JSON格式数据")
            logging.error(f"响应内容: {response.text[:500]}")
            raise Exception("UUTIX项目基础信息API返回非JSON格式数据")
        
        # 检查API响应结构
        if not base_data.get("success", False) or base_data.get("code") != 200:
            error_msg = base_data.get("msg", "未知错误")
            logging.error(f"UUTIX项目基础信息API失败: {error_msg}")
            raise Exception(f"UUTIX项目基础信息API失败: {error_msg}")
        
        project_data = base_data.get("data", {})
        if not project_data:
            logging.error("UUTIX项目基础信息API返回空数据")
            raise Exception("UUTIX项目基础信息API返回空数据")
        
        # 更新项目信息
        self.show_info["show_name"] = project_data.get("name", self.show_info["show_name"])
        
        # 2. 获取演出场次列表
        shows_url = f"https://www.uutix.com/api/oversea/show/list?t={timestamp}&projectId={show_id}&WuKongReady=h5"
        
        response = self.request(shows_url)
        
        if response.status_code != 200:
            logging.error(f"UUTIX演出列表API请求失败: HTTP {response.status_code}")
            raise Exception(f"UUTIX演出列表API请求失败: HTTP {response.status_code}")
        
        try:
            shows_data = response.json()
            logging.info(f"UUTIX演出列表响应: {shows_data}")
        except:
            logging.error("UUTIX演出列表API返回非JSON格式数据")
            raise Exception("UUTIX演出列表API返回非JSON格式数据")
        
        if not shows_data.get("success", False) or shows_data.get("code") != 200:
            error_msg = shows_data.get("msg", "未知错误")
            logging.error(f"UUTIX演出列表API失败: {error_msg}")
            raise Exception(f"UUTIX演出列表API失败: {error_msg}")
        
        shows = shows_data.get("data", [])
        if not shows:
            logging.warning("UUTIX演出列表为空")
            return
        
        # 解析场次信息
        for show in shows:
            show_id_session = show.get("showId")
            show_name = f"{show.get('startTimeDateFormatted', '')} {show.get('startTimeTimeFormatted', '')} {show.get('startTimeWeekFormatted', '')}"
            
            self.show_info["session_info"].append({
                "session_id": str(show_id_session),
                "session_name": show_name.strip(),
                "sale_status": show.get("saleStatus", 0),
                "has_inventory": show.get("hasInventory", False)
            })
            
            # 获取票价信息
            self.get_session_tickets(str(show_id_session), show_name.strip())

    def get_session_tickets(self, session_id: str, session_name: str):
        """获取特定场次的票务信息"""
        show_id = self.show_info.get('show_id')
        
        # 获取当前时间戳
        import time
        timestamp = str(int(time.time() * 1000))
        
        # 尝试获取票价信息的API（基于常见的票务系统结构推测）
        possible_apis = [
            f"https://www.uutix.com/api/oversea/ticket/list?t={timestamp}&showId={session_id}&projectId={show_id}&WuKongReady=h5",
            f"https://www.uutix.com/api/oversea/show/tickets?t={timestamp}&showId={session_id}&WuKongReady=h5",
            f"https://www.uutix.com/api/oversea/project/tickets?t={timestamp}&projectId={show_id}&showId={session_id}&WuKongReady=h5"
        ]
        
        for api_url in possible_apis:
            try:
                response = self.request(api_url)
                
                if response.status_code == 200:
                    try:
                        tickets_data = response.json()
                        
                        if tickets_data.get("success") and tickets_data.get("code") == 200:
                            data = tickets_data.get("data", [])
                            logging.info(f"成功获取场次 {session_id} 票务信息: {tickets_data}")
                            
                            # 解析票务数据
                            if isinstance(data, list):
                                tickets = data
                            elif isinstance(data, dict):
                                tickets = data.get("tickets", data.get("list", []))
                            else:
                                tickets = []
                            
                            for ticket in tickets:
                                ticket_id = ticket.get("ticketId", ticket.get("id"))
                                price = ticket.get("price", ticket.get("ticketPrice", ""))
                                area = ticket.get("area", ticket.get("seatArea", ""))
                                
                                if ticket_id:
                                    self.show_info["seat_info"].append({
                                        "session_id": session_id,
                                        "session_name": session_name,
                                        "seat_plan_id": str(ticket_id),
                                        "seat_plan_name": f"{area} ¥{price}".strip(),
                                    })
                            
                            # 如果成功获取到数据，就不尝试其他API了
                            if tickets:
                                return
                                
                    except Exception as e:
                        logging.warning(f"解析场次 {session_id} 票务JSON失败: {e}")
                else:
                    logging.warning(f"票务API {api_url} 返回HTTP {response.status_code}")
                    
            except Exception as e:
                logging.warning(f"请求票务API {api_url} 失败: {e}")
        
        # 如果所有API都失败，添加一个默认的票务信息
        logging.warning(f"无法获取场次 {session_id} 的具体票务信息，添加默认信息")
        self.show_info["seat_info"].append({
            "session_id": session_id,
            "session_name": session_name,
            "seat_plan_id": session_id,
            "seat_plan_name": "待查询票价",
        })

    def monitor(self) -> list:
        logging.info(f"UUTIX {self.show_info.get('show_name')} 监控中")
        can_buy_list = []
        show_id = self.show_info.get('show_id')
        
        # 获取当前时间戳
        import time
        timestamp = str(int(time.time() * 1000))
        
        # 重新获取演出列表以检查库存状态
        shows_url = f"https://www.uutix.com/api/oversea/show/list?t={timestamp}&projectId={show_id}&WuKongReady=h5"
        
        try:
            response = self.request(shows_url)
            
            if response.status_code == 200:
                try:
                    shows_data = response.json()
                    
                    if shows_data.get("success") and shows_data.get("code") == 200:
                        shows = shows_data.get("data", [])
                        
                        for show in shows:
                            show_id_session = str(show.get("showId", ""))
                            has_inventory = show.get("hasInventory", False)
                            sale_status = show.get("saleStatus", 0)
                            
                            # 检查是否有库存且在售
                            # saleStatus: 1=预售, 2=在售, 3=停售, 4=售罄
                            if has_inventory and sale_status in [1, 2]:
                                can_buy_list.append(show_id_session)
                                logging.info(f"发现可购买场次: {show_id_session}, 库存状态: {has_inventory}, 销售状态: {sale_status}")
                            
                    else:
                        logging.warning(f"监控API响应失败: {shows_data.get('msg', '未知错误')}")
                        
                except Exception as e:
                    logging.warning(f"解析监控API响应失败: {e}")
            else:
                logging.warning(f"监控API请求失败: HTTP {response.status_code}")
                
        except Exception as e:
            logging.warning(f"监控请求失败: {e}")
        
        return can_buy_list

    def request(self, url: str) -> Response:
        return requests.get(
            url=url,
            headers=UUTIX.headers(),
            proxies=self._proxy,
            verify=False,
            timeout=10
        )

    @staticmethod
    def headers():
        return {
            'Host': 'www.uutix.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Origin': 'https://www.uutix.com',
            'Referer': 'https://www.uutix.com/',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Cookie': 'logan_session_token=8kyabcrhiehudecu5rfv; my_lpl_token=MY_e5j2Qf6EUI9LL_juoyMlAL2wp94AAAAw7zwxfcSsYEVGc6d1mFpx31QmLaWejtpevjlUTbm7H2Kwks3Rs3ByRTumnHptJD03AAAAiAAAAAEB',
        }
