require('dotenv').config()
const path = require('path')
const express = require('express')
const bcrypt = require('bcrypt')
const passport = require('passport')
const flash = require('express-flash')
const session = require('express-session')
const bodyParser = require('body-parser')
const sqlite3 = require('sqlite3').verbose()

const initializePassport = require('./authentication')
initializePassport(
    passport, 
    email => users.find(user => user.email === email),
    id => users.find(user => user.id === id)
)

const app = express()

const dbName = path.join(__dirname, '../database', 'film_database.db');

const db = new sqlite3.Database(dbName, err => {
    if (err) {
        return console.error(err.message);
    }
    console.log('Successful connection to the database');
});

const create_database = `CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    year VARCHAR(4) NOT NULL
    );`;


const create_users = `CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(32) NOT NULL
    );`;

db.run(create_database, err => {
    if (err) {
        return console.error(err.message);
    }
    console.log('Successful creation of the films table.');
});

db.run(create_users, err => { 
    if (err) { return console.error(err.message); }
    console.log('Successful creation of the users table.'); 
});


app.use(bodyParser.urlencoded({extended: false}));
app.use(flash())
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false, // Resave session variables if there is no change.
    saveUninitialized: false // Do not save empty values.
}))
app.use(passport.initialize())
app.use(passport.session())

app.set('views', path.join(__dirname, '../views'));
app.set('view engine', 'pug');

app.use(express.static(path.join(__dirname, '../public')));


app.get('/', (request, response, next) => {
    response.render('index', {title: 'home'})    
});

app.get('/login', (request, response, next) => {
    response.render('login', {title: 'login'})    
});

app.post('/login', (request, response, next) => {
})

app.get('/signup', async (request, response, next) => {
    response.render('signup', {title: 'signup'})    
});

app.post('/signup', async (request, response, next) => {
    try {
        const hashedPassword = await bcrypt.hash(request.body.password, 10)
        const user = [request.body.username, request.body.email, hashedPassword];
        const sql = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)';
        db.run(sql, user, err => {
            if (err) {
                console.error(err.message);
            }
        });
        console.log(user);
        response.redirect('/login');
    }
    catch {
        response.redirect('/signup');
    }
});

app.get('/films', (request, response, next) => {
    const sql = 'SELECT * FROM films ORDER BY title'
    db.all(sql, [], (err, rows) => {
        if (err) {
            return console.error(err.message);
        }
        response.render('films', {title: 'films', films: rows})    
    })
});

app.get('/addentry', (request, response, next) => {
    response.render('addentry', { model: {} })
})

app.post('/addentry', (request, response, next) => {
    const sql = 'INSERT INTO films (title, year) VALUES (?, ?)';
    const film = [request.body.title, request.body.year];
    db.run(sql, film, err => {
        if (err) {
            console.error(err.message);
        }
        response.redirect('/films');
    });
});

app.get('/edit/:id', (request, response, next) => {
    const id = request.params.id;
    const sql = 'SELECT * FROM films WHERE id = ?';
    db.get(sql, id, (err, row) => {
        if (err) {
            console.error(err.message);
        }
        response.render('edit', { model: row })    
    });
});

app.post('/edit/:id', (request, response, next) => {
    const id = request.params.id;
    const film = [request.body.title, request.body.year, id];
    const sql = 'UPDATE films SET title = ?, year = ? WHERE (id = ?)';
    db.run(sql, film, err => {
        if (err) {
            console.error(err.message);
        }
        response.redirect('/films');
    })
})

app.get('/delete/:id', (request, response, next) => {
    db.serialize(() => {
        db.run(`DELETE FROM films WHERE id = ?`, request.params.id, err => {
            if (err) {
                console.error(err.message);
            }
            response.redirect('/films');
        })
    })
});

app.use((require, response) => {
    response.status(404).render('error');
});


const server = app.listen(3000, () => {
    console.log(`Server running on ${server.address().port}.`);
});
