import imaplib
import email
from email.header import decode_header
import pandas as pd
from typing import List, Dict, Optional
import os
import re
from datetime import datetime
import openpyxl

class EmailParser:
    """
    邮件解析助手类，用于连接邮箱并解析所有邮件
    支持将解析结果保存到对应文件夹，包括CSV文件和附件
    """

    def __init__(self, email_address: str, password: str, server: str = "imap.mxhichina.com"):
        """
        初始化邮件解析器

        Args:
            email_address: 邮箱地址
            password: 邮箱密码或应用专用密码
            server: IMAP服务器地址，默认为Gmail
        """
        self.email_address = email_address
        self.password = password
        self.server = server
        self.mail = None

    def connect(self) -> bool:
        """
        连接到IMAP服务器

        Returns:
            bool: 连接是否成功
        """
        try:
            self.mail = imaplib.IMAP4_SSL(self.server)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def disconnect(self):
        """
        断开与IMAP服务器的连接
        """
        if self.mail:
            self.mail.close()
            self.mail.logout()

    def get_mailboxes(self) -> List[str]:
        """
        获取所有邮箱文件夹名称

        Returns:
            List[str]: 文件夹名称列表
        """
        if not self.mail:
            raise Exception("未连接到邮箱服务器")

        status, folders = self.mail.list()
        if status != 'OK':
            raise Exception("获取邮箱文件夹失败")

        folder_names = []
        for folder in folders:
            # 解析文件夹名称
            match = re.search(r'"[^"]*"\s*"([^"]*)"', folder.decode())
            if match:
                folder_names.append(match.group(1))

        return folder_names

    def select_folder(self, folder: str = "INBOX") -> int:
        """
        选择邮箱文件夹并返回邮件总数

        Args:
            folder: 文件夹名称，默认为收件箱

        Returns:
            int: 邮件总数
        """
        if not self.mail:
            raise Exception("未连接到邮箱服务器")

        status, messages = self.mail.select(folder)
        if status != 'OK':
            raise Exception(f"选择文件夹 {folder} 失败")

        # 获取邮件总数
        num_messages = int(messages[0])
        return num_messages

    def sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符

        Args:
            filename: 原始文件名

        Returns:
            str: 清理后的文件名
        """
        # 移除或替换非法字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
        clean_name = re.sub(illegal_chars, '_', filename)
        # 限制长度
        if len(clean_name) > 200:
            clean_name = clean_name[:200]
        return clean_name or "unnamed_file"

    def save_attachment(self, part, folder_path: str) -> str:
        """
        保存附件到指定文件夹

        Args:
            part: 邮件附件部分
            folder_path: 保存文件夹路径

        Returns:
            str: 保存的文件路径
        """
        # 获取附件文件名
        filename = part.get_filename()
        if filename:
            # 解码文件名
            filename_parts = decode_header(filename)
            filename = ""
            for part_name, encoding in filename_parts:
                if isinstance(part_name, bytes):
                    filename += part_name.decode(encoding or 'utf-8')
                else:
                    filename += part_name

            # 清理文件名
            filename = self.sanitize_filename(filename)

            # 创建完整路径
            filepath = os.path.join(folder_path, filename)

            # 如果文件已存在，添加序号
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1

            # 保存附件
            try:
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                return filepath
            except Exception as e:
                print(f"保存附件 {filename} 失败: {e}")

        return ""

    def parse_email_content(self, msg, folder_path: str) -> Dict:
        """
        解析单封邮件内容，包括保存附件

        Args:
            msg: email.message对象
            folder_path: 附件保存文件夹路径

        Returns:
            Dict: 解析后的邮件信息
        """
        # 解析邮件头部信息
        subject = msg["Subject"]
        if subject:
            subject, encoding = decode_header(subject)[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')

        from_ = msg.get("From")
        to = msg.get("To")
        date = msg.get("Date")

        # 解析邮件正文
        body_text = ""
        body_html = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # 处理附件
                if "attachment" in content_disposition:
                    attachment_path = self.save_attachment(part, folder_path)
                    if attachment_path:
                        attachments.append(attachment_path)
                    continue

                # 处理正文内容
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        content = payload.decode(charset, errors='ignore')

                        if content_type == "text/plain":
                            body_text += content
                        elif content_type == "text/html":
                            body_html += content
                except Exception as e:
                    print(f"解析邮件正文出错: {e}")
        else:
            content_type = msg.get_content_type()
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    content = payload.decode(charset, errors='ignore')

                    if content_type == "text/plain":
                        body_text = content
                    elif content_type == "text/html":
                        body_html = content
            except Exception as e:
                print(f"解析邮件正文出错: {e}")

        return {
            "subject": subject,
            "from": from_,
            "to": to,
            "date": date,
            "body_text": body_text.strip(),
            "body_html": body_html.strip(),
            "attachments": attachments
        }

    def create_folder_structure(self, base_path: str, folder_name: str) -> str:
        """
        创建文件夹结构

        Args:
            base_path: 基础路径
            folder_name: 邮箱文件夹名称

        Returns:
            str: 创建的文件夹路径
        """
        # 清理文件夹名称
        safe_folder_name = self.sanitize_filename(folder_name)
        folder_path = os.path.join(base_path, safe_folder_name)

        # 创建主文件夹
        os.makedirs(folder_path, exist_ok=True)

        # 创建附件子文件夹
        attachments_path = os.path.join(folder_path, "attachments")
        os.makedirs(attachments_path, exist_ok=True)

        return folder_path

    def fetch_emails(self, folder: str = "INBOX", limit: Optional[int] = None,
                     save_path: str = "./email_results") -> List[Dict]:
        """
        获取并解析指定文件夹中的所有邮件，保存到对应文件夹

        Args:
            folder: 邮箱文件夹名称
            limit: 限制获取的邮件数量，None表示获取所有
            save_path: 保存结果的基础路径

        Returns:
            List[Dict]: 解析后的邮件列表
        """
        if not self.mail:
            raise Exception("未连接到邮箱服务器")

        # 创建文件夹结构
        folder_path = self.create_folder_structure(save_path, folder)
        attachments_path = os.path.join(folder_path, "attachments")

        # 选择文件夹
        total_messages = self.select_folder(folder)
        print(f"文件夹 '{folder}' 中共有 {total_messages} 封邮件")

        # 确定要获取的邮件数量
        count = min(limit, total_messages) if limit else total_messages

        emails = []
        # 按照从新到旧的顺序获取邮件
        for i in range(total_messages, max(0, total_messages - count), -1):
            try:
                # 获取邮件
                status, msg_data = self.mail.fetch(str(i), "(RFC822)")
                if status != 'OK':
                    continue

                # 解析邮件
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        parsed_email = self.parse_email_content(msg, attachments_path)
                        parsed_email['id'] = i
                        emails.append(parsed_email)
                        break

            except Exception as e:
                print(f"获取第 {i} 封邮件时出错: {e}")
                continue

        # 保存CSV文件
        csv_path = os.path.join(folder_path, f"{folder}_emails.csv")
        self.save_to_csv(emails, csv_path)

        return emails

    def save_to_csv(self, emails: List[Dict], filename: str):
        """
        将解析后的邮件保存为CSV文件

        Args:
            emails: 解析后的邮件列表
            filename: 保存的文件名
        """
        # 准备数据，将附件列表转换为字符串
        data = []
        for email_info in emails:
            email_copy = email_info.copy()
            # 将附件列表转换为字符串以便保存到CSV
            if 'attachments' in email_copy:
                email_copy['attachments'] = ';'.join(email_copy['attachments'])
            data.append(email_copy)

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"已保存 {len(emails)} 封邮件到 {filename}")

    def fetch_customs_emails(self, folder: str = "INBOX", limit: Optional[int] = None,
                             save_path: str = "./email_results") -> List[Dict]:
        """
        获取并解析指定文件夹中标题包含"报关资料"且包含"版本号"的邮件，保存到对应文件夹

        Args:
            folder: 邮箱文件夹名称
            limit: 限制获取的邮件数量，None表示获取所有
            save_path: 保存结果的基础路径

        Returns:
            List[Dict]: 解析后的邮件列表
        """
        if not self.mail:
            raise Exception("未连接到邮箱服务器")

        # 创建文件夹结构
        folder_path = self.create_folder_structure(save_path, folder)
        attachments_path = os.path.join(folder_path, "attachments")

        # 选择文件夹
        total_messages = self.select_folder(folder)
        print(f"文件夹 '{folder}' 中共有 {total_messages} 封邮件")

        # 确定要获取的邮件数量
        count = min(limit, total_messages) if limit else total_messages

        emails = []
        processed_count = 0

        # 按照从新到旧的顺序获取邮件
        for i in range(total_messages, max(0, total_messages - count), -1):
            try:
                # 获取邮件
                status, msg_data = self.mail.fetch(str(i), "(RFC822)")
                if status != 'OK':
                    continue

                # 解析邮件
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # 检查邮件主题是否符合条件
                        subject = msg["Subject"]
                        if subject:
                            # 解码主题
                            decoded_subject, encoding = decode_header(subject)[0]
                            if isinstance(decoded_subject, bytes):
                                decoded_subject = decoded_subject.decode(encoding or 'utf-8')

                            # 检查是否包含"报关资料"和"版本号"
                            if "报关资料" in decoded_subject and "版本号" in decoded_subject:
                                parsed_email = self.parse_email_content(msg, attachments_path)
                                parsed_email['id'] = i
                                emails.append(parsed_email)
                                processed_count += 1
                                print(f"找到符合条件的邮件 {processed_count}: {decoded_subject}")
                        break

            except Exception as e:
                print(f"获取第 {i} 封邮件时出错: {e}")
                continue

        # 保存CSV文件
        if emails:
            csv_path = os.path.join(folder_path, f"{folder}_customs_emails.csv")
            self.save_to_csv(emails, csv_path)
            
            # 提取报关资料并保存到Excel
            self.extract_customs_info_to_excel(emails, save_path)

        print(f"总共找到 {len(emails)} 封符合条件的邮件")
        return emails

    def extract_customs_info_to_excel(self, emails: List[Dict], save_path: str = "./email_results"):
        """
        从符合条件的邮件中提取报关资料信息并保存到Excel文件

        Args:
            emails: 解析后的邮件列表
            save_path: 保存结果的基础路径
        """
        customs_data = []
        
        for email_info in emails:
            subject = email_info.get('subject', '')
            body_text = email_info.get('body_text', '')
            
            # 使用正则表达式提取信息
            # 提取提单号 (从主题中)
            bl_no_match = re.search(r'(\d+-\d+)\s+报关资料', subject)
            bl_no = bl_no_match.group(1) if bl_no_match else ''
            
            # 提取其他信息 (从正文中)
            gross_weight_match = re.search(r'提单总毛重[：:]\s*(\d+\.?\d*)\s*KG', body_text)
            gross_weight = gross_weight_match.group(1) if gross_weight_match else ''
            
            cartons_match = re.search(r'大箱个数[：:]\s*(\d+(?:\.\d+)?)\s*个?', body_text)
            cartons = cartons_match.group(1) if cartons_match else ''
            
            packages_match = re.search(r'包裹个数[：:]\s*(\d+(?:\.\d+)?)\s*个?', body_text)
            packages = packages_match.group(1) if packages_match else ''
            
            volume_match = re.search(r'总体积[：:]\s*(\d+\.?\d*)\s*CBM', body_text)
            volume = volume_match.group(1) if volume_match else ''
            
            # 添加到数据列表
            customs_data.append({
                '主题': subject,
                '提单号': bl_no,
                '提单总毛重(KG)': gross_weight,
                '大箱个数': cartons,
                '包裹个数': packages,
                '总体积(CBM)': volume
            })
        
        # 保存到Excel文件
        if customs_data:
            df = pd.DataFrame(customs_data)
            # 创建文件夹结构
            excel_folder_path = os.path.join(save_path, "报关资料")
            os.makedirs(excel_folder_path, exist_ok=True)
            
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_path = os.path.join(excel_folder_path, f"customs_info_{timestamp}.xlsx")
            
            # 保存到Excel
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"已保存报关资料到 {excel_path}")
        else:
            print("没有提取到报关资料信息")

# def main():
#     """
#     主函数示例：如何使用邮件解析助手
#     """
#     # 配置邮箱信息
#     EMAIL_ADDRESS = "qiyz@smartebao.com"
#     PASSWORD = "HHnDyT5v7beJ9Mog"  # 建议使用应用专用密码
#
#     # 创建邮件解析助手实例
#     parser = EmailParser(EMAIL_ADDRESS, PASSWORD)
#
#     try:
#         # 连接到邮箱
#         if not parser.connect():
#             return
#
#         print("成功连接到邮箱")
#
#         # 获取所有文件夹
#         folders = parser.get_mailboxes()
#         print(f"可用的邮箱文件夹: {folders[:5]}...")  # 只显示前5个
#
#         # 解析收件箱中的邮件，保存到指定文件夹
#         emails = parser.fetch_emails(
#             folder="INBOX",
#             limit=1000,  # 限制获取前10封
#             save_path="./email_results"  # 保存到当前目录下的email_results文件夹
#         )
#
#         # 显示结果
#         print(f"\n成功解析 {len(emails)} 封邮件:")
#         for i, email_info in enumerate(emails[:3]):  # 只显示前3封
#             print(f"\n--- 邮件 {i+1} ---")
#             print(f"主题: {email_info['subject']}")
#             print(f"发件人: {email_info['from']}")
#             print(f"日期: {email_info['date']}")
#             if email_info['attachments']:
#                 print(f"附件: {len(email_info['attachments'])} 个")
#             print(f"正文预览: {email_info['body_text'][:100]}...")
#
#     except Exception as e:
#         print(f"处理过程中出现错误: {e}")
#
#     finally:
#         # 断开连接
#         parser.disconnect()




def main():
    """
    主函数示例：如何使用邮件解析助手
    """
    # 配置邮箱信息
    EMAIL_ADDRESS = "qiyz@smartebao.com"
    PASSWORD = "HHnDyT5v7beJ9Mog"  # 建议使用应用专用密码

    # 创建邮件解析助手实例
    parser = EmailParser(EMAIL_ADDRESS, PASSWORD)

    try:
        # 连接到邮箱
        if not parser.connect():
            return

        print("成功连接到邮箱")

        # 解析收件箱中符合条件的邮件，保存到指定文件夹
        emails = parser.fetch_customs_emails(
            folder="INBOX",
            limit=100,  # 限制处理邮件数量
            save_path="./email_results"  # 保存到当前目录下的email_results文件夹
        )

        # 显示结果
        print(f"\n成功解析 {len(emails)} 封符合条件的邮件:")
        for i, email_info in enumerate(emails[:3]):  # 只显示前3封
            print(f"\n--- 邮件 {i+1} ---")
            print(f"主题: {email_info['subject']}")
            print(f"发件人: {email_info['from']}")
            print(f"日期: {email_info['date']}")
            if email_info['attachments']:
                print(f"附件: {len(email_info['attachments'])} 个")
            print(f"正文预览: {email_info['body_text'][:100]}...")

    except Exception as e:
        print(f"处理过程中出现错误: {e}")

    finally:
        # 断开连接
        parser.disconnect()

if __name__ == "__main__":
    main()
