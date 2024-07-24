This is the localhost version of the app. I was having problems with using .env vars in certain areas to make switching between localhost and heroku easier which lead
to me having to hard code some urls. This version has the locahost urls hard coded. Also I think DATABASE_URL points to a local database, etc.

The Procfile may actually attempt to invoke gunicorn rather than the default development server though. The important thing is that the deployed code is correct
and working. 

The assignment was simply to build a web page that would accept real money for a 'product'. They wanted us to use Stripe but I went with paypal instead. I also 
used this project as an excuse to launch my musician website. Additionally we were only taught Flask but I learned Django for this project.

I based the ecommerce code on a tutorial available online from Code With Steps. It used client side paypal integration, which worked when I first did this assignment
but was no longer working when I went to prepare the app for placement in my portfolio. I believe paypal has phased out client side integration due to security
concerns. Therefore I had to learn server side integration and successfully weave that into my existing app, which in part was based on this tutorial. Additionally,
the paypal docs are really tough for a novice to follow since there are layers upon layers of versions, further complicated by the various languages used to implement
the api. It appeared that node.js was favored for server side integration, so I followed a tutorial using that language, even though I have never formally learned
node.js (though I have done a lot of javascript coding). Suffice it to say that putting this all together was quite an ordeal. But I've come out the other side.
