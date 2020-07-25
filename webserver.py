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
                    #get id 
                    get_id = restaurant.id
                    output += "</br>"
                    output += "<a href='http://localhost:8080/restaurant/%s/edit'> Edit </a>" %get_id
                    output+= "</br>"
                    output += "<a href='http://localhost:8080/restaurant/get_id/delete'> Delete </a>"
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

            if self.path.endswith("/edit"):
                restaurantIdPath= self.path.split("/")[2]
                resQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                if resQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output =""
                    output += "<html><body>"
                    output += "<h1>" + resQuery.name +"</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/edit' >" %restaurantIdPath
                    output += "<input name= 'editRestaurant' type = 'text' placeholder = %s >" %resQuery.name
                    output += "<input type = 'submit' value = 'Rename'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
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

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data': 
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('editRestaurant')

                    restaurantIdPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
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