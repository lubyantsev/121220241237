import matplotlib.pyplot as plt
import data_download as dd
import data_plotting as dplt
from data_analysis import calculate_and_display_average_price, notify_if_strong_fluctuations, export_data_to_csv


def main():
    """
    Основная функция, управляющая процессом загрузки, обработки и визуализации данных о биржевых акциях.

    Функция выполняет следующие действия:
    1. Приветствует пользователя и предоставляет информацию о доступных тикерах и периодах.
    2. Запрашивает ввод тикера акции и периода для получения данных.
    3. Запрашивает порог для уведомления о колебаниях цен.
    4. Загружает данные о выбранной акции за указанный период.
    5. Добавляет скользящее среднее к загруженным данным.
    6. Строит и сохраняет график цен закрытия и скользящих средних.
    7. Рассчитывает и отображает среднюю цену закрытия, индекс относительной силы (RSI), MACD и сигнальную линию.
    8. Уведомляет пользователя о сильных колебаниях цен, если они превышают заданный порог.
    """

    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.")

    # Запрос стиля графика
    available_styles = plt.style.available
    print("Доступные стили графика:", available_styles)
    style = input("Выберите стиль графика из доступных: ")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Запрос выбора периода
    use_custom_dates = input("Хотите использовать конкретные даты начала и окончания? (да/нет): ")

    if use_custom_dates.lower() == 'да':
        start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
        end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
        period = None  # Период не нужен, если используются конкретные даты
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        start_date = None  # Параметры дат остаются пустыми
        end_date = None

    # Запрос порога колебаний
    threshold = float(input("Введите порог для уведомления о колебаниях (в процентах): "))

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Calculate additional indicators
    stock_data = dd.calculate_rsi(stock_data)
    stock_data = dd.calculate_macd(stock_data)

    # Plot the data
    # Используем введенные пользователем даты в названии файла
    if use_custom_dates.lower() == 'да':
        filename = f"{ticker}_{start_date}_to_{end_date}.png"
    else:
        filename = f"{ticker}_{period}.png"

    dplt.create_and_save_plot(stock_data, ticker, period, filename, style)

    # Calculate and display the average price
    calculate_and_display_average_price(stock_data)

    # Notify if there are strong fluctuations
    notify_if_strong_fluctuations(stock_data, threshold)

    # Export data to CSV
    export_filename = input("Введите имя файла для экспорта данных (например, 'stock_data.csv'): ")
    export_data_to_csv(stock_data, export_filename)


if __name__ == "__main__":
    main()
