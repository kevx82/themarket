class Products:
    def __init__(self) -> None:
        """
        Initiate all products from every location and put it in a dictionary
        """
        self.dairy = [{"Frico Gouda":1.99},{"Sria Bio Frische Weidemilch":2.09},{"Zott Monte":2.99},{"Meggle Feine Butter":3.49},{"Ben&Jerry's Cookie Dough":6,79}]
        self.spices = [{"Maggi Gemüsebrühe": 2.39},{"Alnatura Meersalz":1.09},{"Ostmann Kräuter der Provence":2.39},{"Pfefferkörner":2.99},{"Muskatnuss":3.59}]
        self.drinks = [{"Powerade Mountain Blast":1.29},{"Ferrari Brut":.69},{"Fanta":.78}, {"Schultheiss Pils":1}, {"Tignanello 2018":184}]
        # TODO: change food to fruit
        self.fruit = [{"Heinz Tomatenketchup":3.39},{"Barilla Lasagne":2.79},{"Gustavo Gusto Pizza":4.89},{"Bonduelle Goldmais":1.89},{"Broccolo":1.99}]
        self.all_products = {"dairy":self.dairy, "spices":self.spices, "drinks": self.drinks,"fruit": self.fruit}