# Klaudia Barabasz 259046
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GNR:

    def __init__(self):
        self.time_file = []  # lista przechowująca czasy obsługi
        self.minutes = []  # lista przechowująca przedziały czasowe w minutach
        self.calls = []  # lista przechowująca intensywność wywołań
        self.end = 0  # zmienna przechowująca pierwszą minutę GNR
        self.start = 0  # zmienna przechowująca ostatnią minutę GNR
        self.gnr = 0  # zmienna przechowująca wartość GNR

        self.menu()  # wywołanie menu

    def menu(self):
        # wyświetlanie interfejsu użytkownika
        self.menu_page = tk.Frame(root)
        self.help_page = tk.Frame(root)
        self.gnr_help_page = tk.Frame(root)

        # wyświetlanie tytułu
        self.title = tk.Label(self.menu_page, text="GNR", font=("Arial", 18), fg="blue")
        self.title.pack(pady=20)

        # wyświetlanie tekstu / przycisku dot. czasu obsługi
        self.time_file_label = tk.Label(self.menu_page, text="Wybierz plik z czasem obsługi")
        self.time_file_label.pack(pady=20)
        self.time_file_button = tk.Button(self.menu_page, text="Wybierz plik", command=self.load_time_file)
        self.time_file_button.pack()

        # wyświetlanie tekstu / przycisku dot. intensywności wywołań
        self.int_file_label = tk.Label(self.menu_page, text="Wybierz plik z intensywnością wywołań")
        self.int_file_label.pack(pady=20)
        self.int_file_button = tk.Button(self.menu_page, text="Wybierz plik", command=self.load_int_file,
                                         state=tk.DISABLED)
        self.int_file_button.pack()

        # wyświetlanie tekstu / przycisku dot. wyświetlania wykresu
        self.plot_label = tk.Label(self.menu_page, text="Wyświetl wykres GNR")
        self.plot_label.pack(pady=20)
        self.plot_button = tk.Button(self.menu_page, text="Wyświetl", command=self.plotting, state=tk.DISABLED)
        self.plot_button.pack()

        # wyświetlanie przycisków dot. pomocy
        self.gnr_help_button = tk.Button(self.menu_page, text="Metoda wyznaczania GNR", command=self.show_gnr_help)
        self.gnr_help_button.pack(pady=30)
        self.help_button = tk.Button(self.menu_page, text="Pomoc", command=self.show_help)
        self.help_button.pack(pady=10)

        # wyświetlanie przycisków dot. autora
        self.author = tk.Label(self.menu_page, text="Autor: Klaudia Barabasz")
        self.author.pack(pady=35)

        self.menu_page.pack()
        self.help_page.pack_forget()
        self.gnr_help_page.pack_forget()

    def help(self):
        # wyświetlanie strony 'Pomoc'
        help_text = '''Program "GNR" służy do wyznaczania godziny największego ruchu 
        telekomunikacyjnego. 
        
        Godzina największego ruchu (GNR) jest to okres kolejnych 60 minut z jednej doby,
        podczas którego występuje maksymalny całkowity ruch telekomunikacyjny.
        
        Jak poprawnie wyznaczyć GNR za pomocą programu?
        1. Wczytaj plik zawierający czas obsługi. 
        
        2. Wczytaj plik zawierający intensywność wywołań. 
        
        3. Po wczytaniu poprawnie obu plików pojawia się możliwość wyświetlenia 
        wykresu GNR. 
        
        (UWAGA! Program przyjmuje jedynie pliki z rozszerzeniem '.txt'. 
        Każda wartość powinna znajdować się w osobnej linjce.
        Plik z intensywnością wywołań powinien zawierać dwie kolumny 
        oddzielone tablatorem.)
        
        Przykład pliku z czasem obsługi:        Przykład pliku z intensywnością:
        '''
        help_text_2 = '158\n9\n9\n3\n11'
        help_text_3 = '\t1\t2,38095E-05\n\t2\t7,14286E-05\n\t4\t2,38095E-05\n\t8\t2,38095E-05\n\t9\t2,38095E-05'

        text = tk.Label(root, text=help_text)
        text.pack()

        main_frame = tk.Frame(root)
        main_frame.pack()

        frame1 = tk.Frame(main_frame, borderwidth=2, relief=tk.GROOVE)
        frame1.pack(padx=10, pady=10, side=tk.LEFT)

        text2 = tk.Label(frame1, text=help_text_2, justify=tk.LEFT)
        text2.pack(padx=20, pady=10)

        gap_frame = tk.Frame(main_frame, width=75)
        gap_frame.pack(side=tk.LEFT)

        frame2 = tk.Frame(main_frame, borderwidth=2, relief=tk.GROOVE)
        frame2.pack(padx=10, pady=10, side=tk.RIGHT)

        text3 = tk.Label(frame2, text=help_text_3, justify=tk.LEFT)
        text3.pack(pady=10)

        button_return = tk.Button(root, text="Powrót", command=self.show_menu)
        button_return.pack(pady=20)

    def gnr_help(self):
        # wyświetlanie strony 'Metoda wyznaczania GNR'
        help_text = '''Metoda wyznaczania GNR:
        1. Wyznaczenie średniego czasu ruchu telekomunikacyjnego
        
        2. Wyznaczenie średniego natężenia ruchu
        
        3. Wyznaczanie godziny największego ruchu
        
            - podzielenie intensywności ruchu telekomunikacyjnego oraz odpowiadających im 
              przedziałów czasowych na 15-minutowe fragmenty
              
            - szukanie największej sumy wartości ruchu z 4 kolejnych fragmentów
        '''

        text = tk.Label(root, text=help_text)
        text.pack()

        button_return = tk.Button(root, text="Powrót", command=self.show_menu)
        button_return.pack(pady=20)

    def show_help(self):
        # przełączanie na stronę 'Pomoc'
        self.help()
        self.menu_page.pack_forget()
        self.help_page.pack()

    def show_gnr_help(self):
        # przełączanie na stronę 'Metoda wyznaczania GNR'
        self.gnr_help()
        self.menu_page.pack_forget()
        self.gnr_help_page.pack()

    def show_menu(self):
        # przełączanie na główną stronę
        for widget in root.winfo_children():
            widget.destroy()
        self.menu()

    def load_time_file(self):
        # wczytywanie pliku z czasem obslugi
        try:
            time_file_path = filedialog.askopenfilename(title="Wybierz plik z czasem obsługi",
                                                        filetypes=(("Dokument tekstowy", "*.txt"),))
            self.time_file = np.loadtxt(time_file_path)
            self.int_file_button.config(state=tk.NORMAL)
        except FileNotFoundError:
            tk.messagebox.showerror("Wystąpił błąd!", "Nie można otworzyć pliku")
        except Exception as error:
            tk.messagebox.showerror("Wystąpił błąd!", str(error))

    def load_int_file(self):
        # wczytywanie pliku z intensywnością wywołań
        try:
            int_file_path = filedialog.askopenfilename(title="Wybierz plik z intensywnością wywołań",
                                                       filetypes=(("Dokument tekstowy", "*.txt"),))
            with open(int_file_path, 'r') as intensity_file:
                for line in intensity_file:
                    self.minutes.append(float(line.strip().split('\t')[0].replace(',', '.')))
                    self.calls.append(float(line.strip().split('\t')[1].replace(',', '.')))
                self.plot_button.config(state=tk.NORMAL)
        except FileNotFoundError:
            tk.messagebox.showerror("Wystąpił błąd!", "Nie można otworzyć pliku")
        except Exception as error:
            tk.messagebox.showerror("Wystąpił błąd!", str(error))

    def average_time(self):
        # wyznaczanie średniego czasu
        return np.average(self.time_file) / 60

    def average_traffic(self):
        # wyznaczanie średniego natężenia ruchu
        return self.average_time() * np.array(self.calls)

    def finding_gnr(self):
        # wyznaczanie GNR
        quarter = 15  # zmienna przechowująca wartość minutową kwadransu
        # podzielenie listy intensywności wywołań na kwadranse
        quarters = [self.calls[i:i + quarter] for i in range(0, len(self.calls), quarter)]
        # podzielenie listy przedziałów czasowych na kwadranse
        quarters_minutes = [self.minutes[i:i + quarter] for i in range(0, len(self.minutes), quarter)]
        # szukanie największej sumy wartości ruchu z 4 kolejnych kwadransów
        for i in range(len(quarters) - 3):
            sum_quarters = sum(quarters[i]) + sum(quarters[i + 1]) + sum(quarters[i + 2]) + sum(quarters[i + 3])
            if sum_quarters > self.gnr:
                self.gnr = sum_quarters
                self.start = int(quarters_minutes[i][0])
                self.end = int(quarters_minutes[i + 3][quarter - 1])
        return self

    def plotting(self):
        # wyświetlenie wykresu
        self.finding_gnr()
        fig, ax = plt.subplots()
        ax.plot(self.minutes, self.average_traffic(), linewidth=1)
        # zaznaczanie GNR na wykresie
        ax.axvspan(self.start, self.end, color='lightgreen')
        ax.set_xlabel("Czas [min]")
        ax.set_ylabel("Średnie natężęnie ruchu")
        ax.set_title("Godzina największego ruchu")
        new_root = tk.Tk()
        new_root.title('Wykres GNR')
        new_root.geometry("1200x600")
        canvas = FigureCanvasTkAgg(fig, master=new_root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plot_data = ''' Wartość GNR: {}
        Przedział czasowy: {}-{} min'''.format(self.gnr, self.start, self.end)
        label = tk.Label(new_root, text=plot_data, font=("Arial", 12))
        label.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("GNR")
    root.geometry('500x550')
    root.resizable(False, False)
    app = GNR()
    root.mainloop()
