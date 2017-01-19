import time

class Orders():
    buyer = {}
    good = {}
    order = {}

    def load_data(self, db):
        f = open("data\\" + db)
        data = f.readlines()
        f.close()
        return data

    def process_data(self, data, type):
        ret = {}
        for i in range(len(data)):
            tmpList = data[i].replace("\n", "").split("\t")
            tmpDict = dict()
            for item in tmpList:
                if item.split(":")[0][0:2] != "a_":
                    tmp = [item.split(":")[0], item.split(":")[1]]
                    tmpDict[tmp[0]] = tmp[1]
            ret[tmpDict.pop(type + "id")] = tmpDict
        return ret

    def load_buyer(self):
        data = self.load_data("buyer.0.0")
        data.extend(self.load_data("buyer.1.1"))
        self.buyer = self.process_data(data, "buyer")


    def load_good(self):
        data = self.load_data("good.0.0")
        data.extend(self.load_data("good.1.1"))
        data.extend(self.load_data("good.2.2"))
        self.good = self.process_data(data, "good")

    def load_order(self):
        data = self.load_data("order.0.0")
        data.extend(self.load_data("order.1.1"))
        data.extend(self.load_data("order.2.2"))
        data.extend(self.load_data("order.0.3"))
        self.order = self.process_data(data, "order")

    def ret_dict_to_str(self, dict):
        ret = ""
        for key in dict:
            ret += key + ": " + dict[key] + "\n"
        return ret

    def __init__(self):
        print "Loading data files..."
        start = time.clock()
        self.load_buyer()
        self.load_good()
        self.load_order()
        print "Loading files done.",
        self.prt_time_consuming(start)

    def prt_time_consuming(self, start):
        print "(Time consuming: " + str(time.clock() - start) + " s.)\n----------------------------------------------------------------\n"

    def prt_orders_number(self):
        start = time.clock()
        print "There're " + str(len(self.order)) + " orders in all.",
        self.prt_time_consuming(start)

    def prt_order_detail(self, orderid):
        start = time.clock()
        if self.order.has_key(orderid):
            #output = ["orderid, buyername, goodname, amount, price, amount * price, time consuming"]
            order = self.order[orderid]
            output = {"orderid" : orderid, "buyername" : self.buyer[order["buyerid"]]["buyername"], "goodname" : self.good[order["goodid"]]["good_name"],
                      "amount" : order["amount"], "price" : self.good[order["goodid"]]["price"]}
            output["amount * price"] = str(float(output["amount"]) * float(output["price"]))
            print self.ret_dict_to_str(output),
        else:
            print "Not found.",
        self.prt_time_consuming(start)

    def ret_buyer_order_info(self, buyerid):
        numret = 0
        moneyret = 0.0
        for orderid in self.order:
            order = self.order[orderid]
            if order["buyerid"] == buyerid:
                numret += 1
                amount = float(order["amount"])
                price = float(self.good[order["goodid"]]["price"])
                moneyret += amount * price
        return [numret, moneyret]

    def prt_buyer_detail(self, buyerid):
        start = time.clock()
        if self.buyer.has_key(buyerid):
            # output = ["buyerid, buyername, the total number of orders, the total amount of payments, time consuming"]
            buyer = self.buyer[buyerid]
            output = {"buyerid": buyerid, "buyername": self.buyer[buyerid]["buyername"]}
            buyerinfo = self.ret_buyer_order_info(buyerid)
            output["the total number of orders"] = str(buyerinfo[0])
            output["the total amount of payments"] = str(buyerinfo[1])
            print self.ret_dict_to_str(output),
        else:
            print "Not found.",
        self.prt_time_consuming(start)

    def ret_good_sale_info(self, goodid):
        numret = 0
        saleret = 0
        for orderid in self.order:
            order = self.order[orderid]
            if order["goodid"] == goodid:
                numret += 1
                saleret += int(order["amount"])
        return [numret, saleret]

    def prt_good_detail(self, goodid):
        start = time.clock()
        if self.good.has_key(goodid):
            # output = ["goodid, goodname, the total number of orders, the total number of saled, time consuming"]
            buyer = self.good[goodid]
            output = {"goodid": goodid, "goodname": self.good[goodid]["good_name"]}
            goodinfo = self.ret_good_sale_info(goodid)
            output["the total number of orders"] = str(goodinfo[0])
            output["the total number of saled"] = str(goodinfo[1])
            print self.ret_dict_to_str(output),
        else:
            print "Not found.",
        self.prt_time_consuming(start)

order = Orders()

command = "5"
while command != "0":
    if command != "5":
        print "------------------------Query Result----------------------------"
    if command == "1":
        order.prt_orders_number()
    elif command == "2":
        order.prt_order_detail(raw_input("Please enter the order id: "))
    elif command == "3":
        order.prt_buyer_detail(raw_input("Please enter the buyer id: "))
    elif command == "4":
        order.prt_good_detail(raw_input("Please enter the good id: "))

    print """1. Calculate the total number of orders
2. Query an order detail by a given orderid
3. Query a buyer' s data by a given buyerid
4. Query a good' s data by a given goodid
0. Exit
"""
    command = raw_input("Please enter the command index: ")