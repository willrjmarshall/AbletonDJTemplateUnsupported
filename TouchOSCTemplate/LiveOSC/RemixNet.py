"""
# Copyright (C) 2007 Nathan Ramella (nar@remix.net)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Nathan Ramella <nar@remix.net> or visit http://www.liveapi.org

RemixNet Module

This module contains four classes that have been assembled to facilitate
remote control of Ableton Live. It's been an interesting experience learning
Python and has given me a lot of time to think about music and networking
protocols. I used OSC as it's somewhat of an accepted protocol and at least
more flexible than MIDI. It's not the quickest protocol in terms of
pure ops, but it gets the job done. 

For most uses all you'll need to do is create an OSCServer object, it
in turn creates an OSCClient and registers a couple default callbacks
for you to test with. Both OSCClient and OSCServer create their own UDP
sockets this is settable on initialization and during runtime if you wish
to change them.

Any input or feedback on this code will always be appreciated and I look 
forward to seeing what will come next.

-Nathan Ramella (nar@remix.net)

-Updated 29/04/09 by ST8 (st8@q3f.org)
    Works on Mac OSX with Live7/8
    
    The socket module is missing on osx and including it from the default python install doesnt work.
    Turns out its the os module that causes all the problems, removing dependance on this module and 
    packaging the script with a modified version of the socket module allows it to run on osx.
    
"""
import sys
import Live

# Import correct paths for os / version
version = Live.Application.get_application().get_major_version()
if sys.platform == "win32":
    import socket   

else:
    if version > 7:
       # 10.5
        try:
            file = open("/usr/lib/python2.5/string.pyc")
        except IOError:
            sys.path.append("/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5")
            import socket_live8 as socket  
        else:
            sys.path.append("/usr/lib/python2.5")
            import socket

import OSC 
      
class OSCClient:
    """
    This is a helperclass for the OSCServer that will setup
    a simple method for sending OSC messages
    """
    
    def __init__(self, udpClient=None, address=None, msg=None):
        """
        Initializes a RemixNet.OSCClient object. You can pass
        in a default address or default msg here. This is useful
        for making 'beacon' clients that you can attach as
        listeners on Live object attributes.
        """
    
        if address is not None:
            self.address = address
            
        if msg:
            self.msg = msg
	else:
	    self.msg = None
            
        if udpClient is not None:
            self.udpClient = udpClient
            
    def setUDPClient(self, udpClient):
        """
        If we create our OSCClient object without defining a udpClient
        we can set one after the fact here. If you don't and you try to
        send, you'll raise an exception.
        """
        
        if udpClient:
            self.udpClient = udpClient
        
    def send(self, address=None, msg=None):
       
        """
        Given an OSC address and OSC msg payload we construct our
        OSC packet and send it to its destination. You can pass in lists
        or tuples in msg and we will iterate over them and append each 
        to the end of a single OSC packet.
        
        This can be useful for transparently dealing with methods that
        yield a variety of values in a list/tuple without the necessity of
        combing through it yourself.
        """
        
        if self.udpClient is None:
            # SHOULD RAISE EXCEPTION
            return
        
        
        # If neither address or msg, we have nothing to do.
        
        if not address and not self.address:
            # SHOULD RAISE EXCEPTION
            return
        
        # I feel a little weird doing this, but I want to keep
        # the 'default' self.msg that the object was initialized
        # with, without playing Towers of Hanoi with another variable.
        
        if self.msg and self.msg is not None:
            msg = self.msg
        
        # I don't like doing it here any more than I did up there.
           
        if not address:
            if not self.address:
                # SHOULD RAISE EXCEPTION
                return
            address = self.address

        oscMessage = OSC.OSCMessage()
        oscMessage.setAddress(address)

        # We need to check for msgs that are actually
        # instance methods here and do something with
        # them...
        # if type(msg) == instance method:
        # blahblah
        
        # By default OSC.py doesn't look like it'll process tuples
        # and pack them. So, we help it along by breaking them up
        # and appending each entity.
       
        if type(msg) in (str,int,float):
           oscMessage.append(msg)
        elif type(msg) in (list,tuple):
             for m in msg:
                if type(m) not in (str,int,float):
                    # SHOULD RAISE EXCEPTION
                    return
                oscMessage.append(m)      
        elif msg == None:
        	self.udpClient.send(oscMessage.getBinary())
		return
        else:
            # SHOULD RAISE EXCEPTION
            # Likely, method or instancemethod object. We should
            # actually execute the code here and send the result,
            # but for now we'll just return.
            return
        # Done processing, send it off to its destination            
       	self.udpClient.send(oscMessage.getBinary())
        
class OSCServer:
        
    def __init__(self, dst=None, dstPort=None, src=None, srcPort=None, ):
        """
        This is the main class we the use as a nexus point in this module.
        
        - dst: destination/target host for OSC responses. If None will default to local network broadcast only.
        - src: Which local interface / ip to bind to, if unset defaults to all
        - srcPort: Source port to bind the server to for incoming OSC queries. Defaults to 9000
        - dstPort: Destination port for OSC responses sent by callbacks. Defaults to 9001       
        
        By default we define and set callbacks for two utility functions that may
        be useful in testing.
        
        /remix/echo -> OSCServer.callbackEcho() - For responding to /remix/echo queries.
        /remix/time -> OSCServer.callbackTime() - Returns time.time() (time in float seconds)
        
        I chose OSC to deliver messages out of necessity, my opinion of OSC at this
        point is that its addressing system is heavyweight although the idea is 
        a reasonable one. But taking into consideration the ratio of address:data
        it becomes somewhat unreasonable unless you take the route of making unreadable
        addresses. As an example I offer the following address,

        /ableton/track/1/volume/set float(0.98)

        To set a single 4 byte float value, we need to use a 27 byte string to get
        it routed to the correct area, and even then we need to make an O(N) comparison
        on the address since we don't have the luxury of a switch statement in Python.
        
        If you're trying to interact with devices in near-realtime the number of ops
        wasted on just getting things to the right place can take the wind out of
        your sails.
        
        But basically for this project to be accepted or useful to anyone it was 
        important to me that we provide a method of accessing that other tools
        could use without having to introduce a new linewire protocol.
        
        It should be noted that performance even with the added ops isn't that bad.
        On my dualcore system I was able to process about 1380 OSC callbacks per
        second. Or, ~86 callbacks per 60ms tick. 
        """

        self.udpServer = UDPServer(src, srcPort)
        self.udpClient = UDPClient(dst, dstPort)
        self.udpClient.open()
        
        self.oscClient = OSCClient(self.udpClient,None, None)
        
        # Create our callback manager and register some utility
        # callbacks to show how its done.
        
        self.callbackManager = OSC.CallbackManager()
        self.callbackManager.add(self.callbackEcho, '/remix/echo')
        self.callbackManager.add(self.callbackEcho, '/remix/time')
        self.udpServer.setCallbackManager(self.callbackManager)
        self.udpServer.bind()
 
    #Should this method go here?
    #def attachToCurrentSongTime(self):
  
    def callbackEcho(self, msg=None):
        """
        When re recieve a '/remix/echo' OSC query from another host
        we respond in kind by passing back the message they sent to us.
        Useful for verifying functionality.
        """
        
        self.oscClient.send('/remix/echo', msg[2])
        
    def callbackTime(self, msg=None):
        """
        When we recieve a '/remix/time' OSC query from another host
        we respond with the current value of time.time()
        
        This callback can be useful for testing timing/queue processing
        between hosts
        """

        self.oscClient.send('/remix/time', time.time())
        
    def sendOSC(self, address=None, msg=None):
        """
        A convienence function so we don't have to dig into the objects
        every time we want to send an OSC packet.
        """
        
        if address and msg:
            self.oscClient.send(address, msg)
    
    def sendUDP(self, data):
        """
        A convienence function so we don't have to dig into the objects
        every time we want to send raw UDP. 
        """
        
        if data:
            self.udpClient.send(data)
            
    def getCallbacks(self):
        """
        If you'd like to see what callbacks you have registered, this function
        will pass you back the dict from the OSC.Manager object.
        """
        
        return dict(self.callbackManager.callbacks)
        
    def addCallback(self, method=None, address=None):
        """
        This method will allow you to externally add callbacks into the 
        UDPServer. As a rule of thumb we'd like to keep everything seperate
        for ease of maintenance.
        
        You call this method with the arguments:
        
        - method: The method object you want to register as a callback for an OSC address.
        - address: The OSC address to bind to. (Example: /remix/mynewcallback/)
        
        If either of these values isn't set, nothing will get registered.
        """
        
        if method and address:
            self.callbackManager.add(method, address)
        else:
            # SHOULD RAISE EXCEPTION?
            return

    def processIncomingUDP(self):
        """
        This is the juice of our tool. While UDP is billed as an unreliable
        protocol, as it turns out it's not that bad. In fact, it can be pretty 
        good.
        
        There are several limitations to the Ableton Live Python environment. 
        
        * The Ableton Live Python environment is minimal. The included module
          list is very short. For instance, we don't have 'select()'.
          
        * The Ableton Live Python version is a bit older than what most Python
          programmers are used to. Its version string says 2.2.1, and the Python
          webpage shows that the offical 2.2.3 came out May 30, 2003. So we've
          got 4 years between us and it. Fortunately since I didn't know any Python
          when I got started on this project the version differences didn't bother 
          me. But I know the lack of modern features has been a pain for a few
          of our developers.
          
        * The Ableton Live Python environment, although it includes the thread
          module, doesn't function how you'd expect it to. The threads appear to
          be on a 100ms timer that cannot be altered consistently through Python.
          
          I did find an interesting behavior in that when you modify the
          sys.setcheckinterval value to very large numbers for about 1-5/100ths of
          a second thread focus goes away entirely and if your running thread is
          a 'while 1:' loop with no sleep, it gets 4-5 iterations in before 
          the thread management stuff kicks in and puts you down back to 100ms 
          loop.
          
          As a goof I tried making a thread that was a 'while 1:' loop with a
          sys.setcheckinterval(50000) inside it -- first iteration it triggered
          the behavior, then it stopped.
          
          It should also be noted that you can make a blocking TCP socket using
          the threads interface. But your refresh is going to be about 40ms slower
          than using a non-blocking UDP socket reader. But hey, you're the boss!
          
          So far the best performance for processing incoming packets can be found
          by attaching a method as a listener to the Song.current_song_time 
          attribute. This attribute updates every 60ms on the dot allowing for 
          16 passes on the incoming UDP traffic every second.
          
          My machine is pretty beefy but I was able to sustain an average of
          over 1300 /remix/echo callback hits a second and only lost .006% 
          of my UDP traffic over 10 million packets on a machine running Live.
          
          One final note -- I make no promises as to the latency of triggers recieved.
          I haven't tested that at all yet. Since the window is 60ms, don't get 
          your hopes up about MIDI over OSC.
        """
        
        self.udpServer.processIncomingUDP()
        
    def bind(self):
        """Bind to the socket and prepare for incoming connections."""
        self.udpServer.bind()
        
    def shutdown(self):
        """If we get shutdown by our parent, close the socket we had open"""
        self.udpClient.close()
        self.udpServer.close()
         
class UDPClient:
    """
    This is a fairly brain-dead UDPClient implementation that is
    used by the OSCClient to send packets out. You shouldn't need
    this unless you want to get tricky or make a linewire protocol.
    """ 
             
    def __init__(self, dst=None, dstPort=None):
        """
        When the OSCClient instantiates its UDPClient it passes along:
        - dst: The destination host. If none only send to localhost.
        - dstPort: The destination port. If none, 9001 by default.
        """
                
        if dst: 
            self.dst = dst 
        else:
            # If you'd like to try broadcast,
            # set this to <broadcast>
            # I've been unable to get it to work.
            self.dst = 'localhost' 
                                   
        if dstPort:               
            self.dstPort = dstPort
        else: 
            self.dstPort = 9001
                        
    def setDstPort(self, dstPort=None):
        """
        If the port gets reset midstream, close down our UDPSock
        and reopen to be sure. A little redundant.
        """

        # Manually set the port before init
        if not dstPort:
            return    
           
        self.DstPort = DstPort
        
        if self.UDPSock:
            self.UDPSock.close()
            self.open()
            
      
         
    def setDst(self, dst=None):
        """
        If the dst gets reset midstream, we close down our UDPSock 
        and reopen. A little redundant.
        """
        
        if not dst:
            return 
        
        self.dst = dst     
        
        if self.UDPSock:
            self.UDPSock.close()
            self.open()
            
      
                
    def open(self):
        """
        Open our UDPSock for listening, sets self.UDPSock
        """
        
        if not self.dst:
            return
        if not self.dstPort:
            return
        
        # Open up our socket, we're ready for business!
        
        self.addr = (self.dst,self.dstPort) 
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
       
        #Broadcast doesn't work for answering callbacks for some reason.
        #But, I'll leave this here if you'd like to try.
        #if self.dst == '<broadcast>':
        #    self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
        
    def send(self, data):
        """
        If we have data to send, send it, otherwise return.
        """
        # Only send if we have data.
        if not data == '':
            self.UDPSock.sendto(data,self.addr)
            data = ''
            
    def close(self):
        """ 
        Close our UDPSock
        """
        # Closing time!
        self.UDPSock.close()
       
class UDPServer:

    """
    RemixNet.UDPServer
       
    This class is a barebones UDP server setup with the ability to
    assign callbacks for incoming data. In the design as is, we use
    an OSC.CallbackManager when we recieve any data.
      
    This class is designed to be used by RemixNet.OSCServer, as it
    will do all the setup for you and register a few default OSCManager
    callbacks.
    """
       
    def __init__(self, src, srcPort):
        """
        Sets up the UDPServer component of this package. By default 
        we listen to all interfaces on port 9000 for incoming requests 
        with a 4096 byte buffer.
        
        You can modify these settings by using the methods setport() and setHost()
        """
        
        if srcPort:
            self.srcPort = srcPort
        else:
            self.srcPort = 9000 
        
        if src:
            self.src = src
        else:
            self.src = ''
        
        self.buf = 4096

    def processIncomingUDP(self):
        """
        Attempt to process incoming packets in the network buffer. If none are
        available it will return. If there is data, and a callback manager has been
        defined we'll send the data to the callback manager. 
        
        You can specify a callback manager using the UDPServer.setCallbackManager() 
        function and passing it a populated OSC.Manager object.
        """
        
        try:
            # You'd think this while 1 loop would get stuck and block the
            # program. But. As it turns out. It doesn't. 
            
            while 1:
                self.data,self.addr = self.UDPSock.recvfrom(self.buf)
                if not self.data:
                # No data buffered this round!
                    return
                else:
                    if self.data != '\n':
                        # Oh snap, we have data!
                        # If you want to write your own special handlers for dealing
                        # with incoming data, this is the place. self.data contains
                        # the raw data sent to our UDP socket.
                
                        if self.callbackManager:
                            self.callbackManager.handle(self.data)
                        
        except Exception, e:
            pass

    def setCallbackManager(self, callbackManager):
        """
        You can specify a callbackManager here as derived from OSC.py. 
        We use this function in OSCServer to register the default /remix/
        namespace addresses as utility callbacks.
        """
        
        self.callbackManager = callbackManager

    def bind(self):
        """
        After initializing you must UDPServer.listen() to bind to the socket
        and accept whatever packets are in the buffer. Since we're binding a 
        non-blocking socket, your program (and Ableton Live) will still be 
        able to run.
        """
        
        self.addr = (self.src,self.srcPort)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDPSock.bind(self.addr)
        self.UDPSock.setblocking(0)

    def close(self):
        """ 
        Close our UDPSock
        """
        # Closing time!
        self.UDPSock.close()
