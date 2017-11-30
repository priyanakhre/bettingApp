import itertools
from pyspark import SparkContext
import MySQLdb
import unicodedata


sc = SparkContext("spark://spark-master:7077", "PopularItems")


data = sc.textFile("/tmp/data/access_log.txt", 2)   


pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], pair[1]))  # 1. Read data in as pairs of (user_id, item_id clicked on by the user)

unique = pages.distinct()  #filter out all duplicate rows in an RDD to produce a new RDD with distinct rows

item_list = unique.groupByKey() # 2. Group data into (user_id, list of item ids they clicked on)

def get_pairs(list):
    pairs = []
    user_id = list[0]
    for item1 in list[1]:
        for item2 in list[1]:
            if (item1 != item2) and (item2>item1):
                pairs.append(((user_id), (item1, item2)))
    return pairs
#3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
pair_items = item_list.flatMap(lambda pair: get_pairs(pair))


#4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
#use opposite of groupByKey() (Group by value)
list_users = pair_items.groupBy(lambda pair: pair[1])


#5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
count_users = list_users.map(lambda pair: ((pair[0]), len(pair[1])) )

#6. Filter out any results where less than 3 users co-clicked the same pair of items

enough_users = count_users.filter(lambda pair: pair[1] >= 3)


output = enough_users.collect()
f=open("/tmp/data/output_log.txt", "a+")
db = MySQLdb.connect("db","www","$3cureUS","cs4501" )
cursor = db.cursor()
sql2 = "Truncate table youbet_reccomendations"

    

cursor.execute(sql2)


db.commit()


for page_id, count in output:
    item1str = page_id[0]
    item2str = page_id[1]
    item1 = int(page_id[0])
    item2= int(page_id[1])

    cursor.execute("""
        INSERT INTO youbet_reccomendations
            (item_id_id,recommended_items)
        VALUES 
            (%s, %s) 
        ON DUPLICATE KEY UPDATE 
                                          -- no need to update the PK 
            recommended_items= CONCAT(recommended_items, ",", %s) ;
                   """, (item1, item2str, item2str)     # python variables
    )
    cursor.execute("""
        INSERT INTO youbet_reccomendations
            (item_id_id,recommended_items)
        VALUES 
            (%s, %s) 
        ON DUPLICATE KEY UPDATE 
                                          -- no need to update the PK 
            recommended_items= CONCAT(recommended_items, ",", %s) ;
                   """, (item2, item1str, item1str)     # python variables
    )    
    db.commit()
    f.write(str(page_id) + '\t' + str(count) + '\n')
    print ("page_id %s count %d" % (str(page_id), count))

print ("Popular items done")
db.close()
sc.stop()