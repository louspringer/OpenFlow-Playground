# Platform Detection and Configuration
# This file handles platform-specific variables and detection

# Platform detection
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
PLATFORM := $(shell echo $(UNAME_S) | tr '[:upper:]' '[:lower:]')
ARCH := $(shell echo $(UNAME_M) | tr '[:upper:]' '[:lower:]')

# Platform-specific variables
ifeq ($(PLATFORM),darwin)
	# macOS
	PACKAGE_MANAGER := brew
	GO_OS := darwin
	GO_ARCH := amd64
	ifeq ($(ARCH),arm64)
		GO_ARCH := arm64
	endif
else ifeq ($(PLATFORM),linux)
	# Linux
	PACKAGE_MANAGER := apt-get
	GO_OS := linux
	GO_ARCH := amd64
	ifeq ($(ARCH),aarch64)
		GO_ARCH := arm64
	endif
else ifeq ($(findstring MINGW,$(UNAME_S)),MINGW)
	# Windows (Git Bash)
	PACKAGE_MANAGER := chocolatey
	GO_OS := windows
	GO_ARCH := amd64
else ifeq ($(findstring MSYS,$(UNAME_S)),MSYS)
	# Windows (MSYS2)
	PACKAGE_MANAGER := pacman
	GO_OS := windows
	GO_ARCH := amd64
else
	# Default to Linux
	PACKAGE_MANAGER := apt-get
	GO_OS := linux
	GO_ARCH := amd64
endif

# Export platform variables
export PLATFORM
export ARCH
export PACKAGE_MANAGER
export GO_OS
export GO_ARCH
