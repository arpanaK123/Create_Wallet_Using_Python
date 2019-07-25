# Import socket module
import socket
import struct
import message_pb2
import messageparam_pb2
import tknCPD_pb2
import txn_pb2
import usrCPD_pb2
import scCPD_pb2
import event_pb2


def client():
    s = socket.socket()
    port = 19000
    s.bind(('', port))
    s.listen()
    while(True):
        conn, addr = s.accept()
        buffer = conn.recv(4024)
        # print(buffer)
        unpack_param = buffer[0:4]
        data = struct.unpack('i', unpack_param)
        print("Total bytes", data)
        txnBytes = buffer[4:8]
        txndata = struct.unpack('i', txnBytes)
        print("No of txns:", txndata)
        cpdBytes = buffer[8:12]
        print("Cpd Total bytes:", cpdBytes)
        reqBytes = buffer[12:]

        resultParse = message_pb2.CPD()
        resultParse.ParseFromString(reqBytes)
        print("result parse", resultParse.command,
              resultParse.params, resultParse.data)

        param = resultParse.params
        resultParam = messageparam_pb2.messageParams()
        resultParam.ParseFromString(param)
        print("outer params: ", resultParam.clientID, " ", resultParam.transactionID, " ",
              resultParam.sessionID, " ", resultParam.status, " ", resultParam.priority)

        print("outer data => inner CPD")
        data = resultParse.data
        innerCpd = message_pb2.CPD()
        innerCpd.ParseFromString(data)
# for create token
      #   resultData = tknCPD_pb2.createToken()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.tokenName, " ", resultData.symbol, " ",
      #         resultData.value, " ", resultData.supply, " ", resultData.timestamp)
# for grant Token
      #   resultData = tknCPD_pb2.grantToken()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.tokenName, " ",
      #         resultData.supply, " ", resultData.timestamp)

# for  modifyClientToken
      #   resultData = tknCPD_pb2.modifyClientToken()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ",
      #         resultData.tokenName, " ", resultData.amount, " ", resultData.timestamp)

#  for checkBalance
      #   resultData = tknCPD_pb2.checkBalance()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ", resultData.tokenName)

# for checkAllowance
      #   resultData = tknCPD_pb2.checkAllowance()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ",
      #         resultData.tokenName, resultData.amount)

# for makeRequest
      #   resultData = tknCPD_pb2.makeRequest()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ",
      #         resultData.tokenName, resultData.amount, " ", resultData.requestID, " ", resultData.sessionID, " ", resultData.timestamp)
# for approveRequest
      #   resultData = tknCPD_pb2.approveRequest()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.requestID, resultData.tokenName, " ", resultData.transactionID, " ", resultData.sessionID, " ",
      #         resultData.approveStatus, resultData.timestamp)

#  for transfer
      #   resultData = tknCPD_pb2.transfer()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ",
      #         resultData.tokenName, resultData.amount, resultData.timestamp)

# for enrollUser
      #   resultData = usrCPD_pb2.enrollUser()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ", resultData.firstName, resultData.lastName,
      #         resultData.address, " ", resultData.dateOfBirth, resultData.policy, resultData.emailID, resultData.password, resultData.securityQuestion, resultData.securityAnswer, resultData.auth, resultData.timestamp)

# for derollment
      #   resultData = usrCPD_pb2.deleteUser()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID)

#  for add smart Contract
      #   resultData = scCPD_pb2.addSmartContract()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.contractName, " ",
      #         resultData.contractFileName, " ", resultData.fileType, " ", resultData.fileMap, " ", resultData.fileContent, " ", resultData.accessControl, " ", resultData.timestamp)


# for read smart contract
        resultData = scCPD_pb2.readSmartContract()
        resultData.ParseFromString(innerCpd.params)
        print("commnad:", innerCpd.command)
        print("params: ", resultData.contractName)


# for Pay
      #   resultData = txn_pb2.txnData()
      #   resultData.ParseFromString(innerCpd.data)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.clientID, " ",
      #         resultData.transactionID, " ", resultData.sessionID, " ", resultData.amount, " ", resultData.receiverID, " ",  resultData.timestamp)


# for event
      #   resultData = event_pb2.evntData()
      #   resultParams = event_pb2.evntParam()
      #   resultData.ParseFromString(innerCpd.data)
      #   resultParams.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command,
      #         " Priority: ", resultParams.priority)
      #   print("params: ", resultData.classID, " ",
      #         resultData.evnetID, " ",  resultData.timestamp)

        # s.close()


client()
