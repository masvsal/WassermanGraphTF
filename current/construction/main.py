import Graph_Loader

#main method
if __name__ == "__main__":
    #open connection
    loader = Graph_Loader.Graph_Loader()

    #initialize database
    loader.test_connection()
    loader.load_entities()
    loader.load_annotations()

    #close connection
    loader.close()