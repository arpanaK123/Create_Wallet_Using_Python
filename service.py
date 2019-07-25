#!/usr/bin/python3
import socket
import random
import struct
import datetime
import message_pb2
import tknCPD_pb2
import messageparam_pb2
import usrCPD_pb2
import scCPD_pb2
import txn_pb2
import event_pb2


def parseData(inputData, clientId):
    innerCmd = inputData["command"]
    innerParams = inputData["params"]
    clientId = int(clientId)

    #  outer params
    txnId, sessionId = randomIds()
    status = '0'

    if innerCmd == "EVENT":
        outerCmd = "SEVT"
        priority = 20

        outerDataBytes = innerCpdLayer(
            innerCmd, innerParams, clientId, txnId, sessionId)
    else:
        outerCmd = "STXN"
        priority = 10

        if innerCmd == "PAY" or innerCmd == "SACT" or innerCmd == "SSCT" or innerCmd == "SREQ" or innerCmd == "SAPP" or innerCmd == "STRA":
            outerDataBytes = innerCpdLayer(
                innerCmd, innerParams, clientId, txnId, sessionId)
        else:
            print("txnid:", txnId)
            outerDataBytes = innerCpdLayer(innerCmd, innerParams)

    outerCmdBytes = outerCmd.encode('utf-8')

    outerParamsBytes = outerParams(
        clientId, txnId, sessionId, status, priority)

    outerCpdBytes = outerCpdLayer(
        outerCmdBytes, outerParamsBytes, outerDataBytes)

    outerCpdBytesLen = len(outerCpdBytes)

    noOfTxn = 1
    txnLenBytes = struct.pack('i', noOfTxn)
    noOfTxnLen = len(txnLenBytes)

    totalBytes = outerCpdBytesLen + noOfTxnLen

    sendToApp(outerCpdBytesLen, outerCpdBytes)

    # Sending Data to CN
    # sendToClientNode(totalBytes, txnLenBytes, outerCpdBytesLen, outerCpdBytes)

    return totalBytes

# generate the random TransactionId and sessionId

def randomIds():
    txnid = random.randint(10000, 20000)
    sessionid = random.randint(20000, 30000)
    return txnid, sessionid


def innerCpdLayer(innerCmd, innerParams, clientId=-1, txnId=-1, sessionId=-1):
    innerCpd = message_pb2.CPD()
    print("innercpd txnid:", txnId)
    dataBytes = None
    if innerCmd == "SCNT":
        paramBytes = createNewToken(innerParams)
    elif innerCmd == "SGRA":
        paramBytes = grantToken(innerParams)
    elif innerCmd == "SACT" or innerCmd == "SSCT":
        paramBytes = modifyClientToken(innerParams, txnId)
    elif innerCmd == "SBAL":
        paramBytes = checkBalance(innerParams)
    elif innerCmd == "SALL":
        paramBytes = checkAllowance(innerParams)
    elif innerCmd == "SREQ":
        paramBytes = makeRequest(innerParams, sessionId)
    elif innerCmd == "SAPP":
        paramBytes = approveRequest(innerParams, txnId, sessionId)
    elif innerCmd == "STRA":
        paramBytes = transfer(innerParams, txnId)
    elif innerCmd == "SUEN":
        paramBytes = enrollUser(innerParams)
    elif innerCmd == "SSUE":
        paramBytes = superUserEnrollment(innerParams)
    elif innerCmd == "SUDE":
        paramBytes = userDerollment(innerParams)
    elif innerCmd == "SASC":
        paramBytes = addSmartContract(innerParams)
    elif innerCmd == "SRSC":
        paramBytes = readSmartContract(innerParams)
    elif innerCmd == "PAY":
        paramBytes, dataBytes = payTransaction(
            innerParams, clientId, txnId, sessionId)
    elif innerCmd == "EVENT":
        paramBytes, dataBytes = registerEvent(
            innerParams, clientId, txnId, sessionId)

    innerCmdBytes = innerCmd.encode('utf-8')
    innerCpd.command = innerCmdBytes
    innerCpd.params = paramBytes
    if dataBytes is not None:
        innerCpd.data = dataBytes
    innerCpdBytes = innerCpd.SerializeToString()

    return innerCpdBytes


def outerParams(clientId, txnId, sessionId, status, priority):
    outerParam = messageparam_pb2.messageParams()

    outerParam.clientID = clientId
    outerParam.transactionID = txnId
    outerParam.sessionID = sessionId
    outerParam.status = status
    outerParam.priority = priority
    print(clientId, txnId, sessionId, status, priority)

    outerParamBytes = outerParam.SerializeToString()
    return outerParamBytes


def outerCpdLayer(outerCommand, outerParams, outerData):
    outerCpd = message_pb2.CPD()
    print(" outer data: ", outerData)
    outerCpd.command = outerCommand
    outerCpd.params = outerParams
    outerCpd.data = outerData

    result = outerCpd.SerializeToString()

    return result


def sendToApp(outerCpdBytesLen, outerCpdBytes):
    buffer = bytearray()
    totalCpdBytesPack = struct.pack("i", outerCpdBytesLen)

    buffer.extend(totalCpdBytesPack)
    buffer.extend(outerCpdBytes)

    s = socket.socket()
    s1 = socket.socket()

    print("Socket successfully created")
    ip = "192.168.1.89"
    port = 19000
    s.connect((ip, port))
    s1.connect(('192.168.1.186', port))

    print('Got connection from')
    print("buffer", buffer)
    s.send(buffer)
    s1.send(buffer)
    s.close()
    s1.close()


def sendToClientNode(totalBytes, txnLenBytes, outerCpdBytesLen, outerCpdBytes):
    buffer = bytearray()
    totalBytesPack = struct.pack("i", totalBytes)
    totalCpdBytesPack = struct.pack("i", outerCpdBytesLen)

    buffer.extend(totalBytesPack)
    buffer.extend(txnLenBytes)
    buffer.extend(totalCpdBytesPack)
    buffer.extend(outerCpdBytes)

    otherSocket = socket.socket()
    mySocket = socket.socket()

    print("Socket successfully created")
    ip = "192.168.1.89"
    port = 19000
    otherSocket.connect((ip, port))
    mySocket.connect(('192.168.1.186', port))

    print('Got connection from')
    print("buffer", buffer)
    otherSocket.send(buffer)
    mySocket.send(buffer)
    otherSocket.close()
    mySocket.close()


def createNewToken(innerParams):
    innerParamsData = tknCPD_pb2.createToken()
    name = innerParams[0]
    innerParamsData.tokenName = name.encode('utf-8')
    symbl = innerParams[1]
    innerParamsData.symbol = symbl.encode('utf-8')
    paramsvalue = float(innerParams[2])
    innerParamsData.value = paramsvalue
    paramssupply = float(innerParams[3])
    innerParamsData.supply = paramssupply
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def grantToken(innerParams):
    innerParamsData = tknCPD_pb2.grantToken()
    name = innerParams[0]
    innerParamsData.tokenName = name.encode('utf-8')
    paramssupply = float(innerParams[1])
    innerParamsData.supply = paramssupply
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def modifyClientToken(innerParams, txnId):
    innerParamsData = tknCPD_pb2.modifyClientToken()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    name = innerParams[1]
    innerParamsData.tokenName = name.encode('utf-8')
    balance = innerParams[2]
    innerParamsData.transactionID = txnId
    innerParamsData.amount = float(balance)
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def checkBalance(innerParams):
    innerParamsData = tknCPD_pb2.checkBalance()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    name = innerParams[1]
    innerParamsData.tokenName = name.encode('utf-8')
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def checkAllowance(innerParams):
    innerParamsData = tknCPD_pb2.checkAllowance()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    name = innerParams[1]
    innerParamsData.tokenName = name.encode('utf-8')
    balance = innerParams[2]
    innerParamsData.amount = float(balance)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def makeRequest(innerParams, sessionId):
    innerParamsData = tknCPD_pb2.makeRequest()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    name = innerParams[1]
    innerParamsData.tokenName = name.encode('utf-8')
    balance = innerParams[2]
    innerParamsData.amount = float(balance)
    innerParamsData.sessionID = sessionId
    requestID = random.randint(30000, 40000)
    innerParamsData.requestID = requestID
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def approveRequest(innerParams, txnId, sessionId):
    innerParamsData = tknCPD_pb2.approveRequest()
    requestId = innerParams[0]
    innerParamsData.requestID = int(requestId)
    approveStatus = innerParams[1]
    innerParamsData.approveStatus = bool(approveStatus)
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    name = innerParams[2]
    innerParamsData.tokenName = name.encode('utf-8')
    innerParamsData.transactionID = txnId
    innerParamsData.transactionID = sessionId
    print("----: ", "re_Id:- ", requestId, "name:- ", name, "status: ",
          approveStatus, "time: ", times, "txnid: ", txnId, "sessionid: ", sessionId)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def transfer(innerParams, txnId):
    innerParamsData = tknCPD_pb2.transfer()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    name = innerParams[1]
    innerParamsData.tokenName = name.encode('utf-8')
    balance = innerParams[2]
    innerParamsData.amount = float(balance)
    times = datetime.datetime.now()
    innerParamsData.transactionID = txnId

    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def enrollUser(innerParams):
    innerParamsData = usrCPD_pb2.enrollUser()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)

    firstName = innerParams[1]
    innerParamsData.firstName = firstName.encode('utf-8')

    lastName = innerParams[2]
    innerParamsData.lastName = lastName.encode('utf-8')

    address = innerParams[3]
    innerParamsData.address = address.encode('utf-8')

    dateOfBirth = innerParams[4]
    innerParamsData.dateOfBirth = dateOfBirth.encode('utf=8')

    password = innerParams[5]
    innerParamsData.password = password.encode('utf-8')

    policy = innerParams[6]
    innerParamsData.policy = policy.encode('utf-8')

    emailID = innerParams[7]
    innerParamsData.emailID = emailID.encode('utf-8')

    securityQuestion = innerParams[8]
    innerParamsData.securityQuestion = securityQuestion.encode('utf-8')

    securityAnswer = innerParams[9]
    innerParamsData.securityAnswer = securityAnswer.encode('utf-8')
    auth = innerParams[10]
    innerParamsData.auth = bool(auth)
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)

    print(cid, address, dateOfBirth, emailID, password,
          securityQuestion, securityAnswer, times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def superUserEnrollment(innerParams):
    innerParamsData = usrCPD_pb2.enrollUser()
    cid = innerParams[0]
    innerParamsData.clientID = int(cid)
    address = innerParams[1]
    innerParamsData.address = address.encode('utf-8')
    dateOfBirth = innerParams[2]
    innerParamsData.dateOfBirth = dateOfBirth.encode('utf=8')
    email = innerParams[3]
    innerParamsData.email = email.encode('utf-8')
    password = innerParams[4]
    innerParamsData.password = password.encode('utf-8')
    securityQuestion = innerParams[5]
    innerParamsData.securityQuestion = securityQuestion.encode('utf-8')
    securityAnswer = innerParams[6]
    innerParamsData.securityAnswer = securityAnswer.encode('utf-8')
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def userDerollment(innerParams):
    innerParamsData = usrCPD_pb2.deleteUser()
    cid = innerParams[0]
    print("clientid: ", cid)
    innerParamsData.clientID = int(cid)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def addSmartContract(innerParams):
    innerParamsData = scCPD_pb2.addSmartContract()
    contractName = innerParams[0]
    innerParamsData.contractName = contractName.encode('utf-8')
    contractFileName = innerParams[1]
    innerParamsData.contractFileName = contractFileName.encode('utf-8')
    fileType = innerParams[2]
    innerParamsData.fileType = fileType.encode('utf-8')
    fileMap = innerParams[3]
    innerParamsData.fileMap = fileMap.encode('utf-8')

    accessControl = innerParams[4]
    innerParamsData.accessControl = accessControl.encode('utf=8')

    fileContent = innerParams[5]
    innerParamsData.fileContent = fileContent
    times = datetime.datetime.now()
    print("datetime:", times)
    innerParamsData.timestamp = str(times)
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def readSmartContract(innerParams):
    innerParamsData = scCPD_pb2.addSmartContract()
    contractName = innerParams[0]
    innerParamsData.contractName = contractName.encode('utf-8')
    paramsBytes = innerParamsData.SerializeToString()

    return paramsBytes


def payTransaction(innerParams, clientId, txnId, sessionId):
    innertxnParam = txn_pb2.txnParam()
    innertxnData = txn_pb2.txnData()
    # inner param
    priority = 10
    innertxnParam.priority = priority
    # inner data
    innertxnData.clientID = clientId
    innertxnData.transactionID = txnId
    innertxnData.sessionID = sessionId
    rcvId = innerParams[0]
    innertxnData.receiverID = int(rcvId)
    amount = innerParams[1]
    innertxnData.amount = float(amount)

    times = datetime.datetime.now()
    print("datetime:", times)
    innertxnData.timestamp = str(times)

    innerTxnParamsBytes = innertxnParam.SerializeToString()
    innerTxnDataBytes = innertxnData.SerializeToString()

    return innerTxnParamsBytes, innerTxnDataBytes


def registerEvent(innerParams, clientId, txnId, sessionId):
    innerEvntParam = event_pb2.evntParam()
    priority = 20
    innerEvntParam.priority = priority

    innerEvntData = event_pb2.evntData()
    classID = innerParams[0]
    innerEvntData.classID = int(classID)
    evnetID = innerParams[1]
    innerEvntData.evnetID = int(evnetID)
    times = datetime.datetime.now()
    print("datetime:", times)
    innerEvntData.timestamp = str(times)

    eventParamsBytes = innerEvntParam.SerializeToString()
    eventDataBytes = innerEvntData.SerializeToString()

    return eventParamsBytes, eventDataBytes
