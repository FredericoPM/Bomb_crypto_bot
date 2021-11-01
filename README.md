O bot funciona epenas no python 3.8.2 e é extremamente sensivel a resolução, então certifiquese que seu pc esta com a escala em 100% (para olhar essa configuração clique com o botão direito na area de trabalho, va em configuração de exibição e estara la) alem disso provavelmente sera necessario tirar todos os prints existentes na pasta images novamente no computador onde o bot sera rodado.

Windows:
	Instalando o bot:
		Instalar o python 3.8.2 (arquivo de instalação esta na pasta windows dentro da pasta do bot, *marque a opção de adicionar o python ao path*)
		python ./windows/get-pip.py (deve ser rodado dentro da pasta do bot)
		pip install pyautogui
		pip install opencv-python
		python bot.py (starta o bot, deve ser rodado dentro da pasta do bot)

Linux:
	Instalando o bot:
		sudo apt-get update
		sudo apt install make
		sudo apt-get install gcc g++
		sudo apt install zlib1g-dev
		sudo apt-get install scrot
		wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
		tar -xf Python-3.8.2.tgz
		cd Python-3.8.2
		./configure --enable-optimizations
		make -j 8
		sudo make altinstall
		sudo apt-get install python3-tk python3-dev
		sudo apt install python3-pip
		python3 -m pip install pyautogui
		python3 -m pip install opencv-python
		
		python3 bot.py (starta o bot, deve ser rodado dentro da pasta do bot)
		
	Instalar Chrome :
		wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
		sudo apt install ./google-chrome-stable_current_amd64.deb