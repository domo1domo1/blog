from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import time
import os
import random
from dotenv import load_dotenv
import pyautogui

pyautogui.FAILSAFE = True  # 안전장치 활성화

class TistoryManager:
    def __init__(self):
        load_dotenv()
        self.blog_name = os.getenv('BLOG_NAME')
        self.initialize_driver()
        
    def initialize_driver(self):
        """브라우저 초기화 및 설정"""
        try:
            options = webdriver.ChromeOptions()
            EXTENSION_PATH = os.path.join(os.getcwd(), 'buster_extension')
            options.add_argument(f'--load-extension={EXTENSION_PATH}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-notifications')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            # options.add_argument('--incognito') # 시크릿 모드
            options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.0.0 Safari/537.36')
            # 자동화 감지 방지 옵션 추가
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)            
            self.driver = uc.Chrome(options=options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            self.browser = webdriver.Chrome(options=options)
            print("브라우저 초기화 완료")
        except Exception as e:
            print(f"브라우저 초기화 실패: {str(e)}")
            raise

    def randomize_window_size(self):
        """창 크기 랜덤화"""
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        self.driver.set_window_size(width, height)

    def random_delay(self, min_sec=2, max_sec=5):
        """자연스러운 지연 시간"""
        time.sleep(random.uniform(min_sec, max_sec))

    def handle_recaptcha(self):
        """reCAPTCHA 처리"""
        try:
            print("reCAPTCHA 감지됨, 처리 중...")
            self.random_delay(2, 3)
            
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in frames:
                try:
                    if "recaptcha" in frame.get_attribute("src").lower():
                        self.driver.switch_to.frame(frame)
                        checkbox = self.wait.until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
                        )
                        self.click_element_safely(checkbox)
                        break
                except:
                    continue
            
            self.driver.switch_to.default_content()
            self.random_delay(5, 7)
            return True
            
        except Exception as e:
            print(f"reCAPTCHA 처리 중 오류: {str(e)}")
            self.driver.switch_to.default_content()
            return False

    def click_element_safely(self, element):
        """요소를 안전하게 클릭"""
        try:
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                return True
            return False
        except Exception as e:
            print(f"클릭 중 오류: {str(e)}")
            return False

    def login(self):
        """티스토리 로그인"""
        try:
            print("로그인 시작...")
            self.driver.get('https://www.tistory.com/auth/login')
            self.random_delay(2, 3)

            # 카카오 로그인 버튼 클릭
            print("카카오 로그인 버튼 클릭...")
            self.driver.find_element(By.CSS_SELECTOR, '.link_kakao_id').click()
            self.random_delay(2, 3)

            # 이메일 입력
            print("이메일 입력...")
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            email_input.send_keys(os.getenv('KAKAO_ID'))
            self.random_delay(1, 2)

            # 비밀번호 입력
            print("비밀번호 입력...")
            pw_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            pw_input.send_keys(os.getenv('KAKAO_PW'))
            self.random_delay(1, 2)

            # 로그인 버튼 클릭
            print("로그인 버튼 클릭...")
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()

            # reCAPTCHA 로딩을 위한 충분한 대기 시간
            print("reCAPTCHA 로딩 대기 중...")
            time.sleep(5)  # 5초 대기

            # reCAPTCHA 처리
            if not self.handle_recaptcha():
                print("reCAPTCHA 처리 실패")
                return False

            return True

        except Exception as e:
            print(f"로그인 중 오류 발생: {str(e)}")
            return False

    def handle_recaptcha(self):
        """reCAPTCHA 처리"""
        try:
            print("reCAPTCHA 처리 중...")
            time.sleep(2)  # 추가 대기 시간

            # reCAPTCHA 체크박스 이미지 찾기
            checkbox_location = None
            try:
                # 체크박스 이미지 파일의 경로를 지정해주세요
                checkbox_location = pyautogui.locateOnScreen('recaptcha_checkbox.png', confidence=0.8)

                if checkbox_location:
                    print("체크박스 발견")
                    # 체크박스 중앙 좌표 계산
                    checkbox_x = checkbox_location.left + (checkbox_location.width / 2)
                    checkbox_y = checkbox_location.top + (checkbox_location.height / 2)

                    # 체크박스 클릭
                    pyautogui.click(checkbox_x, checkbox_y)
                    print("체크박스 클릭 완료")
                    time.sleep(2)

                    return True
                else:
                    print("체크박스를 찾을 수 없습니다")
                    return False

            except Exception as e:
                print(f"이미지 인식 실패: {str(e)}")
                return False

        except Exception as e:
            print(f"reCAPTCHA 처리 중 오류: {str(e)}")
            return False

    def move_to_admin_page(self):
        """관리자 페이지로 이동"""
        try:
            self.driver.get(f'https://{self.blog_name}.tistory.com/manage')
            self.random_delay(2, 3)
            return True
        except Exception as e:
            print(f"관리자 페이지 이동 중 오류: {str(e)}")
            return False

    def create_post(self, title, content, tags):
        """새 포스트 작성"""
        try:
            print("포스트 작성 시작...")
            # 글쓰기 버튼 클릭
            write_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_write'))
            )
            self.click_element_safely(write_button)
            self.random_delay()

            # 제목 입력
            title_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.textarea_tit'))
            )
            self.natural_type(title_field, title)

            # HTML 모드로 전환
            html_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_html'))
            )
            self.click_element_safely(html_button)
            self.random_delay()

            # 내용 입력
            content_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.textarea_inner'))
            )
            self.natural_type(content_field, content)

            # 태그 입력
            tag_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.tag_inp'))
            )
            self.natural_type(tag_field, ', '.join(tags))

            # 발행 버튼 클릭
            publish_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_publish'))
            )
            self.click_element_safely(publish_button)
            self.random_delay(3, 5)

            print("포스트 작성 완료!")
            return True

        except Exception as e:
            print(f"포스트 작성 중 오류 발생: {str(e)}")
            return False

    def close(self):
        """브라우저 종료"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                print("브라우저가 정상적으로 종료되었습니다.")
        except Exception as e:
            print(f"브라우저 종료 중 오류 발생: {str(e)}")