import random
import time
import os
from web3 import Web3
from eth_account import Account
from colorama import Fore, Style, init
import shutil

# Khởi tạo colorama
init(autoreset=True)

# Cấu hình mạng
network_url = "https://rpc.testnet.soniclabs.com"
chain_id = 64165
private_key = ""  # Nhập Private Key của bạn
explorer_url = "https://testnet.soniclabs.com/tx/0x"  # URL cơ sở cho explorer

# Kết nối đến mạng Sonic Testnet
web3 = Web3(Web3.HTTPProvider(network_url))

# Kiểm tra kết nối
if not web3.is_connected():
    raise Exception("Không thể kết nối đến mạng")

# Lấy địa chỉ từ private key
account = Account.from_key(private_key)
sender_address = account.address

# Hàm hiển thị banner
def _banner():
    print(r"""


.▄▄ ·        ▐ ▄ ▪   ▄▄· ▄▄▌   ▄▄▄· ▄▄▄▄· .▄▄ ·     ▄▄▄▄▄▄▄▄ ..▄▄ · ▄▄▄▄▄ ▐ ▄ ▄▄▄ .▄▄▄▄▄
▐█ ▀. ▪     •█▌▐███ ▐█ ▌▪██•  ▐█ ▀█ ▐█ ▀█▪▐█ ▀.     •██  ▀▄.▀·▐█ ▀. •██  •█▌▐█▀▄.▀·•██  
▄▀▀▀█▄ ▄█▀▄ ▐█▐▐▌▐█·██ ▄▄██▪  ▄█▀▀█ ▐█▀▀█▄▄▀▀▀█▄     ▐█.▪▐▀▀▪▄▄▀▀▀█▄ ▐█.▪▐█▐▐▌▐▀▀▪▄ ▐█.▪
▐█▄▪▐█▐█▌.▐▌██▐█▌▐█▌▐███▌▐█▌▐▌▐█ ▪▐▌██▄▪▐█▐█▄▪▐█     ▐█▌·▐█▄▄▌▐█▄▪▐█ ▐█▌·██▐█▌▐█▄▄▌ ▐█▌·
 ▀▀▀▀  ▀█▄▀▪▀▀ █▪▀▀▀·▀▀▀ .▀▀▀  ▀  ▀ ·▀▀▀▀  ▀▀▀▀      ▀▀▀  ▀▀▀  ▀▀▀▀  ▀▀▀ ▀▀ █▪ ▀▀▀  ▀▀▀ 


    """)
    print(Fore.GREEN + Style.BRIGHT + "SONICLABS TESTNET")
    print(Fore.RED + Style.BRIGHT + "Liên hệ: https://t.me/thog099")
    print(Fore.BLUE + Style.BRIGHT + "Replit: Thog")
    print("")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lựa chọn ngôn ngữ
def select_language():
    while True:
        print()
        print("Chọn ngôn ngữ:")
        print("1. Tiếng Việt")
        print("2. English")
        choice = input("Nhập lựa chọn (1/2): ")

        if choice == '1':
            return 'vi'
        elif choice == '2':
            return 'en'
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2.")
            print()

# Tin nhắn dựa trên ngôn ngữ
def get_messages(language):
    if language == 'vi':
        return {
            'success': "✅ Giao dịch thành công! Liên kết: {}",
            'failure': "❌ Giao dịch thất bại. Liên kết: {}",
            'sender': "📤 Địa chỉ người gửi: {}",
            'receiver': "📥 Địa chỉ người nhận: {}",
            'amount': "💸 Số lượng S đã gửi: {} S",
            'gas': "⛽ Gas đã sử dụng: {}",
            'block': "🗳️  Số khối: {}",
            'balance': "💰 Số dư hiện tại: {} S",
            'total': "🏆 Tổng giao dịch thành công: {}",
            'amount_prompt': "Nhập số lượng S muốn gửi (mặc định 0.000001, tối đa 0.0001): "
        }
    else:  # English
        return {
            'success': "✅ Transaction successful! Link: {}",
            'failure': "❌ Transaction failed. Link: {}",
            'sender': "📤 Sender address: {}",
            'receiver': "📥 Receiver address: {}",
            'amount': "💸 Amount S sent: {} S",
            'gas': "⛽ Gas used: {}",
            'block': "🗳️  Block number: {}",
            'balance': "💰 Current balance: {} S",
            'total': "🏆 Total successful: {}",
            'amount_prompt': "Enter the amount of S to send (default 0.000001, maximum 0.0001): "
        }

# Lựa chọn số lượng token
def select_amount(language):
    messages = get_messages(language)
    while True:
        try:
            amount = float(input(messages['amount_prompt']) or 0.000001)
            if 0 < amount <= 0.0001:
                return amount
            else:
                print("Số lượng không hợp lệ. Số lượng phải lớn hơn 0 và không quá 0.0001.")
        except ValueError:
            print("Dữ liệu không hợp lệ. Vui lòng nhập số.")

# Hàm gửi giao dịch
def send_transaction(to_address, amount):
    # Tạo giao dịch
    nonce = web3.eth.get_transaction_count(sender_address)  # Sử dụng `get_transaction_count`
    tx = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(to_address),  # Đảm bảo địa chỉ ở dạng checksum
        'value': web3.to_wei(amount, 'ether'),  # Số lượng S sẽ gửi
        'gas': 21000,  # Giới hạn gas cho giao dịch đơn giản
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id
    }

    # Ký giao dịch
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Gửi giao dịch
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Chờ giao dịch được đưa vào khối
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex(), tx_receipt, amount

# Địa chỉ ngẫu nhiên với checksum
def get_random_address():
    random_address = '0x' + ''.join(random.choices('0123456789abcdef', k=40))
    return Web3.to_checksum_address(random_address)

# Hàm chính
def main():
    total_tx = 0
    successful_tx = 0
    header_displayed = False

    language = select_language()
    messages = get_messages(language)

    amount = select_amount(language)

    try:
        while True:
            if not header_displayed:
                _clear()  # Xóa màn hình trước khi hiển thị banner
                _banner()  # Hiển thị banner chỉ một lần
                header_displayed = True

            to_address = get_random_address()
            tx_hash, tx_receipt, sent_amount = send_transaction(to_address, amount)

            # Loại bỏ tiền tố "0x" từ hash giao dịch
            tx_hash_no_prefix = tx_hash[2:]
            tx_link = explorer_url + tx_hash_no_prefix  # Tạo liên kết txHash không có "0x"

            # Định dạng số lượng S đã gửi
            formatted_amount = f"{sent_amount:.6f}"

            # Hiển thị thông tin bổ sung
            if tx_receipt['status'] == 1:
                successful_tx += 1
                # Lấy số dư hiện tại
                current_balance = web3.eth.get_balance(sender_address)
                # Định dạng số dư hiện tại
                formatted_balance = f"{web3.from_wei(current_balance, 'ether'):.6f}"
                # Hiển thị thông tin bổ sung với biểu tượng và màu sắc
                print(messages['success'].format(Fore.GREEN + tx_link + Style.RESET_ALL))
                print(messages['sender'].format(sender_address))
                print(messages['receiver'].format(Web3.to_checksum_address(to_address)))
                print(messages['amount'].format(formatted_amount))
                print(messages['gas'].format(tx_receipt['gasUsed']))
                print(messages['block'].format(tx_receipt['blockNumber']))
                print(messages['balance'].format(formatted_balance))
                print(messages['total'].format(successful_tx))
            else:
                print(messages['failure'].format(Fore.GREEN + tx_link + Style.RESET_ALL))
                print(messages['sender'].format(sender_address))
                print(messages['receiver'].format(Web3.to_checksum_address(to_address)))
                print(messages['amount'].format(formatted_amount))

            # Thêm dòng trống giữa các giao dịch
            print()

            # Tạm dừng 2 giây giữa các giao dịch
            time.sleep(2)

    except KeyboardInterrupt:
        print("Bot đã dừng lại.")

if __name__ == "__main__":
    main()
