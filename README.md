# Introduksjon til dotfiler

## 🧑‍🍳 Fremgangsmåte

Nå skal vi sette opp våre helt egne dotfiler, og sette opp et bittelite installasjonsscript
for å styre dette. Det anbefales å legge dotfiler-mappen i home-mappa, sånn passe lett tilgjengelig.
Jeg bruker `~/.dotfiles-macos`.

Du kan begynne med å lage en mappe der!

Vi skal flytte en del filer, også på kommandolinja. Da kan det være greit å være kjent med `mv` som er
en kommando for å flytte filer.

```
mv source target
```

og `open` som åpner filer eller mapper.

```
open <FILE>/<FOLDERNAME>
```

### 🧑‍💻 Shell/Bash og terminal-innstillinger

Litt avhengig av hvilken shell man bruker så er det litt forskjellige filer som er i bruk for innstillinger!
Er du usikker på hvilket shell du bruker kan du kjøre kommandoen

```
echo $SHELL
```

- Hvis du bruker `zsh` så finner du innstillingene dine i `.zshrc` på i hjem-mappa
- Hvis du bruker `bash` så finner du innstillingene dine i `.bashrc` eller `.bash_profile`

Vi blir å ha bruk for å vite _hvor_ dotfiles-mappa vår ligger. Så må du lage en environment-variabel der som har ruta til dotfilene dine.

Disse kan begge legges i dotfiles-mappa, og man lager en symlink fra `$DOTFILES/.zshrc` til `~/.zshrc`

Legg til dette i toppen av `rc`-fila di:

```
export DOTFILES="~/.dotfiles-macos/zshrc"
```

> [!TIP]
> For å sjekke om det funker, kan du kjøre følgende kommandoer
>
> `source ~/.dotfiles-macos/.zshrc`
>
> `echo $DOTFILES/` // /Users/jon/.dotfiles-macos/

#### Andre shell-filer

Hvis du har mye greier i fila di her, kan dette være et fint tidspunkt å dele den litt opp.
Jeg har delt min opp i følgende underfiler:

- `.path` for ting som skal legges til på `$PATH` variabelen
- `.alias` for å ha diverse aliaser

Disse kan du enkelt laste inn ved å legge de til i `.zshrc`/`.bashrc`

```
source $DOTFILES/.path
source $DOTFILES/.alias
```

### 🤖 Installasjons-config

For å gjøre det enklere å ha kontroll på plassene man skal flytte filene til, og
hvilke kommandoer man må kjøre for å sette opp dotfilene ligger det et lite python3-script tilgjengelig.
Dette leser av [`config.json`](config.json)-filen og kjører kommandoer og symlinker.

Skriptet forventer at du har en environment-variabel `DOTFILES` satt med filstien til dotfiles-mappa di.

Scriptet kan kjøres med `./install.py`

Du kan kopiere `install.py` og `config.json` herfra og inn i mappa di!

### 🍺 Brew

[Brew](https://brew.sh/) er en package-manager til macOs. Her kan man både installere verktøy,
men også apper og programmer.

```
brew update
```

Og så oppdatere alle brews:

```
brew upgrade
```

og så legge til støtte for `brew bundle` som hjelper med å lage en `Brewfile`

```
brew tap homebrew/bundle
```

#### Å lage seg en brewfile

En `Brewfile` er en fil med en liste med `Brews` (CLI-verktøy), `Taps` (Tredje-parts pakker)
og `Casks` (GUI-programmer).Filen kan brukes for å installere, rydde opp og oppdatere pakkene
du _vet_ at du skal ha på plass i oppsettet ditt.

Du kan se hvilke pakker du har installert med

```
brew list
```

For å eksportere alle disse til en `Brewfile` kan du kjøre

```
brew bundle dump
```

Her er det nok lurt å ta en liten gjennomgang, og fjerne eventuelle avhengigheter
du _ikke_ ønsker å alltid ha installert.

> [!TIP]
> Hvis du vil rydde litt i ettertid, kan man kjøre kommandoen under for å slette
> _alt_ annet en det som ligger i Brewfila
>
> `brew bundle cleanup`

#### Å bruke brewfila fra dotfiles!

`brew bundle` leter i utgangspunktet kun etter en `Brewfile` i nærmeste mappe.
Du kan sende inn en fil med flagget `--file`, og kan peke den på din dotfiles-Brewfile med `brew bundle --file $DOTFILES/Brewfile`

```
brew bundle --file $DOTFILES/Brewfile
```

Alle brew-kommandoene kan være greit å pakke med i `config.json`, så de er klare hvis du skal kjøre `install.py`😸 Du kan se eksempel [her](https://github.com/jonjohansen/.dotfiles-macos/blob/main/config.json)

### 🐙 `git`-innstillinger

Det er alltid kjekt å ha innstillingene sine for `git` med seg.
Disse finner du som regel i en fil på rot i home-mappa (`~`) og heter den heter `.gitconfig`.

Du kan også ha en global gitignore som kan være grei å ha med seg. For å lage dette kan du kjøre kommandoene

```
touch ~/.gitignore
```

```
git config --global core.excludesfile ~/.gitignore
```

### 🖥️ iTerm

Hvis du brukes iTerm kan du finne innstillingene dine for dette i på `~/Library/Preferences/com.googlecode.iterm2.plist`

iTerm har også en mulighet for å bytte hvor innstillingene lastes fra. Det betyr at istedenfor at man trenger å symlinke
innstillingene ut fra dotfiles-mappa, kan man heller sette innstillingen til å lese av settingene rett fra dotfilene dine.

1. Kopier `~/Library/Preferences/com.googlecode.iterm2.plist` til dotfilene dine
2. Spesifiser den nye pathen til innstillingene med

```
defaults write com.googlecode.iterm2.plist PrefsCustomFolder -string "<PATH>";
```

og sett innstillingen for å bruke egen config-path med

```
defaults write com.googlecode.iterm2.plist LoadPrefsFromCustomFolder -bool true;
```

Hvis du bruker et veldig spesielt tema som du ønsker å ha med, kan du legge dette også i dotfiles-mappa di, og bare gå inn i innstillinger i iTerm og legge det til derfra!

> [!TIP]
> Hvis du syns det var litt vanskelig å huske, kan du også lage et lite shell-script som gjør akkurat dette, og heller kjøre scriptet en hver av kommandoene.
> [Eksempel](https://github.com/jonjohansen/.dotfiles-macos/blob/be92344096a6134d2133856b87cfdfb3fd261b6e/iterm2/config)

### 👻 ghostty

Hvis du har hoppet på den nye trendye terminalen [ghostty](https://ghostty.org/) så er det minimalt med oppsett.
Du legger config-filen (som du finner på `$HOME/.config/ghostty/config`) i dotfiles-mappa di, også symlinker du den til `$HOME/.config/ghostty/config`

### 🍎 macOs

Har du lyst å ta det _enda_ et hakk lengre, kan du også automatisere innstillingene dine fra maccen.
Disse kan settes gjennom kommandoer, og for enkelhets skyld kan du pakke de sammen i en liten shell-scriptfil du kjører. Denne kan også legges til i `config.json` ✌️

Mange innstillinger finner du på [macos-defaults](https://macos-defaults.com/)
og ser f.eks ut som denne for å bytte scrolle-retning:

```
defaults write NSGlobalDomain com.apple.swipescrolldirection -bool false
```

## 🤠 Mine dotfiler

Du kan også snike og se på mine dotfiler på [her](https://github.com/jonjohansen/.dotfiles-macos)
