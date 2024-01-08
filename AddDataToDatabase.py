import firebaseCreds as fc

data = {
    '14512':{
        "name" : "SS Rajamouli",
        "major" : "Film direction",
        "starting_year" : 2018,
        "total_attendance" : 0,
        "standing" : "GG",
        "year" : "3",
        "last_attended_time" : "2023-12-11 14:23:12"

    },
    '41235':{
        "name" : "Elon Musk",
        "major" : "Building spaceships and fast cars",
        "starting_year" : 2016,
        "total_attendance" : 0,
        "standing" : "GG",
        "year" : "4",
        "last_attended_time" : "2023-12-11 17:32:45"

    },
    '67891':{
            "name" : "Nisarg Mehta",
            "major" : "Software engg",
            "starting_year" : 2019,
            "total_attendance" : 0,
            "standing" : "GG",
            "year" : "3",
            "last_attended_time" : "2023-12-11 09:23:34"
        }
}

for key,val in data.items():
    fc.ref.child(key).set(val)

