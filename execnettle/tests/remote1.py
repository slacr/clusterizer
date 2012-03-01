"""
This is a test module that we can send as a parameter to remotely exec on a
gateway.
"""

if __name__ == '__channelexec__':
	channel.send("initialization complete")
