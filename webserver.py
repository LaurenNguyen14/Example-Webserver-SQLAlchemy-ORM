from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys

#import CRUD operations
from database_setup import Base, Restaurant, MenuItem 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

#create session and connect to Db 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession(); 


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all();
                #list all names of restaurants
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
          

                output = ""
                output +="<html><body>"
                output +=  "<a/ href = 'http://localhost:8080/restaurants/new'> Add a new restaurant</a>"
                output += "</br>"
                output += "</br>"

                for restaurant in restaurants: 
                    output+= restaurant.name #get the name of the restaurant entity
                    output += "</br>"
                    output += "<a href='http://localhost:8080/restaurant/id/edit'> Edit </a>"
                    output+= "</br>"
                    output += "<a href='http://localhost:8080/restaurant/id/delete'> Delete </a>"
                    output+= "</br>"

                output +="</body></html>"
                self.wfile.write(output)
                print output
                return 

              


            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
            	self.send_response(200)
            	self.send_header('Content-type','text/html')
            	self.end_headers()
            	output = ""
            	output += "<html><body>"
            	output += "<h1>Make a new restaurant </h1>"
            	output += "<form method = 'POST' enctype = 'multipart/form-data' action ='/restaurants/new' >"
            	output += "<input name = 'newRestaurant' type='text' placeholder ='New Restaurant Name'>"
            	output+="	<input type = 'submit' value = 'Create' ></form>"

            	output +="</body></html>"
                self.wfile.write(output)
                #print output
            	return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
        	if self.path.endswith("/restaurants/new"):
        		ctype, pdict = cgi.parse_header(
                	self.headers.getheader('content-type'))
            	if ctype == 'multipart/form-data':
                	fields = cgi.parse_multipart(self.rfile, pdict)
                	messagecontent = fields.get('newRestaurant')

                	# Create new Restaurant Object
                	newRestaurant = Restaurant(name = messagecontent[0])
                	session.add(newRestaurant)
                	session.commit()

                	self.send_response(301)
            		self.send_header('Content-type', 'text/html')
            		self.end_headers()

                	
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()