CFLAGS := -std=c++17 -g -Wall -pedantic
C := g++

MKDIRCMD := mkdir 

SRCDIR := src/backend
BINDIR := bin
EXENAME := sstp-backend

FILES = $(wildcard $(SRCDIR)/*.cpp)
NPFILES = $(patsubst $(SRCDIR)/%,%,$(FILES))
OBJS = $(addprefix bin/,$(patsubst %.cpp,%.o,$(NPFILES)))
HEADERS = $(wildcard $(SRCDIR)/*.h)

ifeq ($(OS),Windows_NT)
	MKDIRCMD += $(BINDIR)
else
	MKDIRCMD += -p $(BINDIR)
endif

symb: $(OBJS)
	@-$(MKDIRCMD)
	$(C) -o $(BINDIR)/$(EXENAME) $(CFLAGS) $(OBJS) -I$(SRCDIR)

$(OBJS): $(BINDIR)/%.o: $(SRCDIR)/%.cpp $(HEADERS)
	@-$(MKDIRCMD)
	$(C) -c $(patsubst $(BINDIR)/%,$(SRCDIR)/%,$(patsubst %.o,%.cpp,$@)) -o $@ $(CFLAGS)

clean:
	rm -f $(BINDIR)/$(EXENAME)
	rm -f $(BINDIR)/*.o