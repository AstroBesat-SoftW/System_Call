from kutuphaneler import *
from api_key import *


# Log dosyasını ve seviyesini yapılandırıyoruz
logging.basicConfig(
    filename='system_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

from log_sistem_verileri import *

# Uygulamayı çalıştır
root.mainloop()
