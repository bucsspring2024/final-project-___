from src.sample_controller import main_menu, main, play



def main():
    run = main_menu(), play(), 
    # run = Bullet(), Hero(), Enemy()
    run = main()
    run.main()

main()



# def main():
#     pygame.init()
#     #Create an instance on your controller object
#     #Call your mainloop
    
#     ###### NOTHING ELSE SHOULD GO IN main(), JUST THE ABOVE 3 LINES OF CODE ######

# # https://codefather.tech/blog/if-name-main-python/
# if __name__ == '__main__':
#     main()
