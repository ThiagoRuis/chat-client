set -e

mongo <<EOF
use admin

db.createUser(
    {
        user: '$APP_MONGO_USER',
        pwd: '$APP_MONGO_PASS',
        roles: [
            {
                role: "readWrite",
                db: '$APP_DATABASE'
            }
        ]
    }
);

conn2 = new Mongo();
db = conn2.getDB('$APP_DATABASE');
db.Message.insert(
    { "text": "Initialized Chat" }
);
EOF