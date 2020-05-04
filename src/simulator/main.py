from obc import On_Board_Computer
from uart_test import Stm_Uart
from spi_test import Stm_Spi
from ethernet_test import Stm_Ethernet

if __name__ == "__main__":
    obc = On_Board_Computer()
    stm_uart = Stm_Uart()
    stm_spi = Stm_Spi()
    stm_ethernet = Stm_Ethernet()

    obc.start()
    stm_spi.start()
    stm_uart.start()
    stm_ethernet.start()
