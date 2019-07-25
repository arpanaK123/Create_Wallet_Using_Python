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


def App():
    s = socket.socket()
    port = 19000
    s.bind(('', port))
    s.listen()
    while(True):
        conn, addr = s.accept()
        buffer = conn.recv(4024)
        # print(buffer)
      #   totalBytes, txnLenBytes, outerCpdBytesLen, outerCpdBytes
        unpack_param = buffer[0:4]
        data = struct.unpack('i', unpack_param)
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
        resultData = tknCPD_pb2.createToken()
        resultData.ParseFromString(innerCpd.params)
        print("commnad:", innerCpd.command)
        print("params: ", resultData.tokenName, " ", resultData.symbol, " ",
              resultData.value, " ", resultData.supply, " ", resultData.timestamp)
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
      #         resultData.tokenName, resultData.amount)
# for approveRequest
      #   resultData = tknCPD_pb2.approveRequest()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.requestID, " ",
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
      #   print("params: ", resultData.clientID, " ",
      #         resultData.address, " ", resultData.dateOfBirth, " ", resultData.email, " ", resultData.password, " ", resultData.securityQuestion, " ", resultData.securityAnswer, " ", resultData.timestamp)

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
      #         resultData.contractFileName, " ", resultData.fileType, " ", resultData.fileMap, " ", resultData.accessControl, " ", resultData.timestamp)


# for read smart contract
      #   resultData = scCPD_pb2.readSmartContract()
      #   resultData.ParseFromString(innerCpd.params)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.contractName)


# for txn
      #   resultParams=txn_pb2.txnParam()

      #   resultData = event_pb2.evntData()
      #   resultData.ParseFromString(innerCpd.data)
      #   print("commnad:", innerCpd.command)
      #   print("params: ", resultData.classID, " ",
      #         resultData.evnetID,  resultData.timestamp)

        # s.close()


App()
