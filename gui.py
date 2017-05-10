"""A simple Dashboard gui for displaying the Time, Weather and News"""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from tkinter import ttk

import push_bullet as pb
import weather
from subreddit_scraper import SubScraper


class DashboardLauncher:
    """Launcher for the main Dashboard
    allows the user to set location and start or close the app"""

    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to Dashboard")
        self.master.geometry("350x55+200+200")
        self.master.resizable(False, False)

        self.dashboard_window = None

        self.launcher_header = ttk.Frame(master)
        self.launcher_header.pack()

        ttk.Label(self.launcher_header,
                  text="Enter Your Location or Postcode",
                  padding=2).pack()

        self.launcher_input_frame = ttk.Frame(master)
        self.launcher_input_frame.pack()

        self.input_var = tk.StringVar()
        self.user_input = ttk.Entry(self.launcher_input_frame,
                                    textvariable=self.input_var,
                                    width=15)

        self.user_input.pack(side=tk.LEFT, ipadx=25)

        self.start_b = ttk.Button(self.launcher_input_frame,
                                  text="Start",
                                  command=self.launch_dashboard)

        self.start_b.pack(side=tk.LEFT, padx=10)

        self.stop_b = ttk.Button(self.launcher_input_frame,
                                 text="Stop",
                                 state=tk.DISABLED,
                                 command=self.quit_dashboard)

        self.stop_b.pack(side=tk.RIGHT)

    def launch_dashboard(self):

        try:
            self.dashboard_window = tk.Toplevel(self.master)
            db = Dashboard(self.dashboard_window, self.input_var.get())
            self.user_input.state(['disabled'])
            self.start_b.state(['disabled'])
            self.stop_b.state(['!disabled'])

        except KeyError:
            messagebox.showerror("Error", "Location not valid\n"
                                          "Try again")
            self.user_input.delete(0, 'end')
            self.quit_dashboard()

    def quit_dashboard(self):
        self.dashboard_window.destroy()
        self.start_b.state(['!disabled'])
        self.stop_b.state(['disabled'])
        self.user_input.state(['!disabled'])


class Dashboard:
    """Main interface for the Dashboard"""

    def __init__(self, master, location):
        """
        :param master:  Dashboards parent obj
        :param location: User input location 
        """
        self.weather = weather.Weather(location)

        self.master = master
        self.master.geometry("1024x600")
        self.master.title(self.weather.raw_weather_data["name"])
        self.master.resizable(True, True)
        # For enabling/disabling window decorations
        self.master.overrideredirect(False)
        self.master.configure(background="black")

        # variables for weather data that is to be displayed
        self.weather_d = tk.StringVar()
        self.weather_img = tk.PhotoImage()
        self.weather_t = tk.StringVar()

        # variables for date and time data that is to be displayed
        self.current_time = tk.StringVar()
        self.current_date = tk.StringVar()
        self.current_day = tk.StringVar()

        # file path
        self.file_p = "./icons/{}.png"

        # dynamically created widgets are stored in theses lists
        self.day_labels = []
        self.temp_labels = []
        self.icon_labels = []

        # r/subreddit, 2nd argument = number of stories to scrape
        self.news_data = SubScraper("worldnews", 5)
        self.story_labels = []

        # Styling Stuff
        l_style = ttk.Style()
        l_style.configure("L.TLabel",
                          background="black",
                          foreground="white",
                          font=("Roboto", 14))

        f_style = ttk.Style()
        f_style.configure("F.TFrame",
                          background="black",
                          foreground="white",
                          borderwidth=0)

        # ---- LEFT FRAME ----

        self.left_frame = ttk.Frame(master,
                                    style="F.TFrame",
                                    height=600,
                                    width=450)

        self.left_frame.grid(column=0, row=0, sticky="e")
        self.left_frame.grid_propagate(0)

        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        # Grid template for Weather Frame
        self.weather_frame = ttk.Frame(self.left_frame,
                                       style="F.TFrame")

        self.weather_frame.grid(column=0, row=0, sticky="s")

        # weather icon, measurement and description interfaces

        self.weather_img_label = ttk.Label(self.weather_frame,
                                           style="L.TLabel",
                                           image=self.weather_img)

        self.weather_measurement_label = ttk.Label(self.weather_frame,
                                                   textvariable=self.weather_t,
                                                   style="L.TLabel",
                                                   font=("Roboto", 14))

        self.weather_description_label = ttk.Label(self.weather_frame,
                                                   textvariable=self.weather_d,
                                                   style="L.TLabel",
                                                   wraplength=200,
                                                   font=("Roboto", 20))

        self.weather_img_label.grid(row=0, column=1, sticky="n")
        self.weather_measurement_label.grid(row=0, column=2, sticky="w")
        self.weather_description_label.grid(row=1, column=1, sticky="n")

        # Grid template for Date and Time interfaces

        self.date_time_frame = ttk.Frame(self.left_frame,
                                         style="F.TFrame")

        self.date_time_frame.grid(column=0, row=1, sticky="n")

        #  TIME and DATE interfaces

        self.current_time_label = ttk.Label(self.date_time_frame,
                                            style="L.TLabel",
                                            font=("Roboto", 52),
                                            textvariable=self.current_time)

        self.current_date_label = ttk.Label(self.date_time_frame,
                                            style="L.TLabel",
                                            font=("Roboto", 20),
                                            textvariable=self.current_date)

        self.current_day_label = ttk.Label(self.date_time_frame,
                                           style="L.TLabel",
                                           font=("Roboto", 20),
                                           textvariable=self.current_day)

        self.current_time_label.grid(rowspan=2, padx=20, sticky="w")
        self.current_day_label.grid(row=0, column=1, sticky="s")
        self.current_date_label.grid(row=1, column=1, sticky="n")

        # ---- MIDDLE FRAME ----

        self.middle_frame = ttk.Frame(master,
                                      style="F.TFrame",
                                      height=600,
                                      width=50)

        self.middle_frame.grid(row=0, column=1, sticky="e")

        # buttons for switching between forecast and news tab

        tk.Button(self.middle_frame,
                  text="°C",
                  foreground="white",
                  background="black",
                  bd=0,
                  highlightthickness=0,
                  activeforeground="#00FFFF",
                  activebackground="black",
                  font=("Roboto", 16, "bold"),
                  command=self.call_forecast).grid(row=0, pady=10, sticky="e")

        tk.Button(self.middle_frame,
                  text="☶",
                  foreground="white",
                  background="black",
                  bd=0,
                  highlightthickness=0,
                  activeforeground="#00FFFF",
                  activebackground="black",
                  font=("Roboto", 16),
                  command=self.call_news
                  ).grid(row=1, pady=10, sticky="e")

        # Undecided Button for additional tab/features

        # tk.Button(self.middle_frame,
        #           text="???",
        #           bd=0,
        #           foreground="white",
        #           background="black",
        #           activeforeground="#00FFFF",
        #           activebackground="black",
        #           font=("Segoe UI Light", 16),
        #           command=None).grid(row=0, padx=5, pady=5)

        # ---- RIGHT FRAME ----

        self.right_frame = ttk.Frame(master,
                                     style="F.TFrame",
                                     height=600,
                                     width=524)

        self.right_frame.grid(row=0,
                              column=2,
                              sticky="e")

        self.right_frame.columnconfigure(0, minsize=524)

        self.right_frame.grid_propagate(0)

        # forecasts and weather are displayed on a tabbed frame
        # using styles to blend the tabbed interface into the background

        self.forecast_tab = ttk.Frame(self.right_frame,
                                      style="F.TFrame")

        # widgets for forecast created here
        for days in range(0, 3):
            day = ttk.Label(self.forecast_tab,
                            style="L.TLabel")
            day.grid(row=days, column=0, padx=60, pady=60, sticky="e")
            self.day_labels.append(day)

            icon = ttk.Label(self.forecast_tab,
                             style="L.TLabel")
            icon.grid(row=days, column=1, pady=60)
            self.icon_labels.append(icon)

            temp = ttk.Label(self.forecast_tab,
                             style="L.TLabel",
                             font=("Roboto", 12))
            temp.grid(row=days, column=2, padx=60, pady=60, sticky="w")
            self.temp_labels.append(temp)

        self.forecast_tab.grid(sticky="e")

        # widgets for news created here

        self.news_tab = ttk.Frame(self.right_frame,
                                  style="F.TFrame",
                                  height=600)

        for stories in range(0, self.news_data.no_of_stories):
            self.news_tab.grid_rowconfigure(stories, weight=1)

            story = tk.Button(self.news_tab,
                              wraplength=400,
                              justify="left",
                              highlightthickness=0,
                              bd=0,
                              foreground="white",
                              background="black",
                              activeforeground="#00FFFF",
                              activebackground="black",
                              font=("Roboto", 12))

            self.story_labels.append(story)
            story.grid(row=stories, column=0, pady=25, sticky="w")

        self.news_tab.grid(sticky="nes")

        self.update_date_time()  # function keeps date_time frame updated
        self.update_weather()  # function keeps weather updated
        self.update_forecast()  # function keeps forecast updated
        self.update_news()  # function keeps news updated
        self.call_forecast()  # gui defaults to forecast

    def update_date_time(self):
        """
        :return: sets/updates the time and date for the main widget
        """
        d_now = datetime.now()
        # updates time
        self.current_time.set(d_now.strftime("%H : %M"))

        # updates date
        self.current_date.set(d_now.strftime("%d %B %Y"))

        # updates current day
        self.current_day.set(d_now.strftime("%A"))

        # delay to update date_time frame (milliseconds)
        self.date_time_frame.after(10000, self.update_date_time)

    def update_weather(self):
        """
        :return: sets/updates the weather icon, description and measurement 
        data
        """

        t_now = datetime.now().strftime("%H:%M:%S")
        self.weather.request_data()

        s_rise = self.weather.sun_moon("rise")
        s_set = self.weather.sun_moon("set")
        we_id = self.weather.get_weather("id")
        night_id = ["800", "801", "802"]

        # updates the weather icon based on sunrise and sunset
        if ((t_now < s_rise) == (t_now < s_set)) and (we_id in night_id):
            self.weather_img.config(file=self.file_p.format(we_id + "n"))
        else:
            self.weather_img.config(file=self.file_p.format(we_id))

        self.weather_img_label.config(image=self.weather_img)
        self.weather_img_label.image = self.weather_img

        # updates weather description
        self.weather_d.set(self.weather.get_weather("description"))

        # updates weather measurement
        self.weather_t.set(self.weather.get_weather("temperature"))

        # delay to update master_frame (milliseconds)
        self.weather_frame.after(1200000, self.update_weather)

    def update_forecast(self):
        """
        :return: sets/updates the forecast widgets data
        """

        # updates forecast
        self.weather.request_data()

        for day_l in self.day_labels:
            counter = self.day_labels.index(day_l) + 1
            day = datetime.now() + timedelta(days=counter)
            day_l.config(text=day.strftime("%A"))

        for temp_l in self.temp_labels:
            counter = self.temp_labels.index(temp_l) + 1
            temp = self.weather.forecast(counter)["temperature"]
            temp_l.config(text=temp)

        for ico in self.icon_labels:
            counter = self.icon_labels.index(ico) + 1
            img = tk.PhotoImage(
                file=self.file_p.format(
                    self.weather.forecast(counter)["id"])).subsample(2, 2)
            ico.config(image=img)
            ico.img = img

        self.forecast_tab.after(1200000, self.update_forecast)

    def update_news(self):
        """    
        :return: sets/updates the news/subreddit widgets data
        """

        # News updates
        self.news_data.fetch_data()

        for n_labels in self.story_labels:
            counter = self.story_labels.index(n_labels)
            n_labels.config(
                text=self.news_data.data[counter][0],
                command=lambda i=counter: self.push(self.news_data.data[i]))

        self.news_tab.after(1800000, self.update_news)

    def call_forecast(self):
        """
        
        :return: hides the news frame and shows the forecast frame
        """
        self.news_tab.grid_remove()
        self.forecast_tab.grid()

    def call_news(self):
        """
        
        :return: hides the forecast frame and shows the news frame
        """
        self.forecast_tab.grid_remove()
        self.news_tab.grid()

    @staticmethod
    def push(item):
        """
        Pushbullet
        :param item: combination of news story title and link
        :return: pushes to mobile device
        """
        story = item[0]
        link = item[1]
        pb.push_message(story, link)


def main():
    root = tk.Tk()
    db_launcher = DashboardLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
