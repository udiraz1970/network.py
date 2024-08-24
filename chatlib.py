# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data) -> str:
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
    # Implement code ...
	if len(cmd) > 16 or len(data) > MAX_DATA_LENGTH:
		return None

	return cmd.ljust(CMD_FIELD_LENGTH) + '|' + '{:04d}'.format(len(data)) + '|' + data


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
    # Implement code ...

    # The function should return 2 values
    #return cmd, msg
	msg_list = data.split('|')
	try:
		if len(msg_list) != 3:
			return None, None
		elif len(msg_list[2]) != int(msg_list[1]):
			return None, None
		else:
			return msg_list[0].strip(), msg_list[2]
	except ValueError:
		return None, None


	
def split_data(msg, expected_fields) -> list:
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	# Implement code ...

	l = msg.split('#')
	if len(l) - 1 == expected_fields:
		for i, item in enumerate(l):
			try:
				l[i] = int(item)
			except ValueError:
				try:
					l[i] = float(item)
				except ValueError:
					pass
		return l
	else:
		return None


def join_data(msg_fields) -> str:
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	# Implement code ...
	return '#'.join([str(item) for item in msg_fields])
