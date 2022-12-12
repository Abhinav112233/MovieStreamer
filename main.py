import time
import pyautogui
from tkinter import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class GUI():

    def __init__(self):
        window = Tk()
        window.title("Movie Streamer")
        frame1 = Frame(window)
        frame1.pack()
        labTitle = Label(frame1, text="Enter the name of movie")
        self.movieTitle = StringVar()
        entryTitle = Entry(frame1, textvariable=self.movieTitle)
        labTitle.grid(row=6, column=10, columnspan=4)
        entryTitle.grid(row=16, column=10, columnspan=3)
        frame2 = Frame(window)
        frame2.pack()
        btn = Button(frame2, text="Fetch", fg="red", command=self.processbtn)
        btn.grid(row=0, column=6)
        frame3 = Frame(window)
        frame3.pack()
        self.statusLabel = Label(frame3, text="Searching for the movie")
        self.statusLabel.grid(row=0, column=8)
        window.mainloop()

    def processbtn(self):

        movie = self.movieTitle.get()
        movie = movie.title()

        df = pd.read_csv("user_data.csv")
        movies = df["MOVIES"].values.tolist()
        movies.append(movie)
        df = pd.DataFrame(movies, columns=['MOVIES'])
        print(df)
        df.to_csv("user_data.csv", index=False)

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.implicitly_wait(20)

        browser.get("https://soap2day.sh/")

        browser.find_element(By.XPATH, '//*[@id="btnhome"]').click()

        input = browser.find_element(By.XPATH, '//*[@id="txtSearch"]')
        input.send_keys(movie)
        input.send_keys(Keys.ENTER)
        try:
            movie_thumbnail = browser.find_element(By.CSS_SELECTOR,
                                                   "body > div > div:nth-child(3) > div > div.col-sm-8.col-lg-8.col-xs-12 > div:nth-child(1) > div.panel-body > div > div > div > div > div:nth-child(1) > div:nth-child(2)")
            movie_thumbnail.click()

            stream = browser.find_element(By.XPATH,
                                          '/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div[5]/div[2]/div[1]/div[2]/div[12]/div[1]/div/div/div[2]/div')
            stream.click()
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'w')
            pyautogui.press("f")

            time.sleep(10000)



        except:
            print("oops")


GUI()
