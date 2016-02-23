#encoding=utf-8
import time

import win32gui
import win32con
import win32process


_test_env = False 

def GetText(hwnd):
    buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    buffer = win32gui.PyMakeBuffer(buf_size)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
    return buffer[:buf_size]


def SetText(hwnd, text):
    win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)


def click(hwnd, lparamHexstr):
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, int(lparamHexstr, 16))
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, int(lparamHexstr, 16))


def processenum(hwnd, param_list):
    if win32gui.GetClassName(hwnd) == param_list[0] and win32gui.IsWindowVisible(hwnd):
        param_list[1] = hwnd
        return False
    return True


def get_sure_hwnd(threadid):
    param_list = []
    param_list.append('TImageCodeForm')
    param_list.append('')

    if _test_env:
        param_list[0] = 'TImageForm'

    while True:
        time.sleep(0.2)
        try:
            win32gui.EnumThreadWindows(threadid, processenum, param_list)
            if param_list[1]:
                return param_list[1]
        except:
            if param_list[1]:
                return param_list[1]




def get_error_hwnd(threadid):
    param_list = []
    param_list.append('TErrorBoxForm')
    param_list.append('')

    try:
        win32gui.EnumThreadWindows(threadid, processenum, param_list)
        return param_list[1]
    except:
        return param_list[1]

def clear_error(threadid):
    hd = get_error_hwnd(threadid)
    if hd:
        click(hd, '00E20116')

def get_bid_price(parenthwnd):
    hwnd = 0
    while True:	
    	hwnd = win32gui.FindWindowEx(parenthwnd, hwnd, "TNoPasteEdit", None)
	if win32gui.IsWindowVisible(hwnd):
	    break

    
    if hwnd:
    	#title= win32gui.GetWindowText(hwnd)
	title= GetText(hwnd)
	print hex(hwnd), title
	clear_title = ''
	for c in title:
	    if c != '\x00':
		    clear_title +=c
	print repr(clear_title)
	return int(clear_title)
    print u"未获取出价窗口句柄".encode('gbk')	

if __name__ == '__main__':
    current_price = 0
    a1 = win32gui.FindWindow("TMainForm", None)
    if not a1:
        print u"请先启动国拍客户端".encode('gbk')
    else:
        e1 = win32gui.FindWindowEx(a1, None, "TNoPasteEdit", None)

	while True:
		if  win32gui.IsWindowVisible(e1):
			break;
		else:
	            e1 = win32gui.FindWindowEx(a1, e1, "TNoPasteEdit", None)
	print hex(e1)
			
        # e2 = win32gui.FindWindowEx(a1, e1, "TEdit", None)
        threadid, processid = win32process.GetWindowThreadProcessId(a1)
	print (u"threadid， processid： %s %s" % (threadid, processid)).encode('gbk')
        while True:
            try:
		#no = raw_input(u'是否开始投标: 回车确认， 任意键清除错误窗口\r\n'.encode('gbk'))
               	#if not no:
		    clear_error(threadid)
		    #print u"点击 +300 开始".encode('gbk')
		    #click(a1, '01680297')
		    #print u"点击 +300 完成".encode('gbk')	
		    #time.sleep(0.2)
		    #bid_price = int(get_bid_price(a1))
		    #print (u"出价 --- 已出价 ：%i --- %i" % (bid_price, current_price)).encode('gbk')
		    #if  bid_price > current_price:
		    price = raw_input(u"输入当前中标价\r\n".encode('gbk'))
		    print price
		    bid_price = str(int(price) * 100 + 800)
		    print bid_price
		    SetText(e1, bid_price)
		    print u"点击 出价 开始".encode('gbk')
		    click(a1, '0199032E')
		    print u"点击 出价 完成".encode('gbk')
		    print u"获取验证码窗口句柄 开始".encode('gbk')
		    ac_hwnd = get_sure_hwnd(threadid)
		    print u"获取验证码窗口句柄 结束".encode('gbk')
                    e = win32gui.FindWindowEx(ac_hwnd, None, "TEdit", None)
                    sure_code = raw_input(u"校验码:".encode('gbk'))
                    SetText(e, sure_code)
		    #raw_input(u'确认校验码已输入窗口'.encode('gbk'))
		    print u"提交 开始".encode('gbk')
                    click(ac_hwnd, '00DE009F')
		    print u"提交 结束".encode('gbk')
		    #current_price = bid_price
		    #else:
		    #	print u"该价格已出价".encode('gbk')
		    #raw_input(u"回车清除提交成功窗口".encode('gbk'))
		    clear_error(threadid)
		#else:
		    #clear_error(threadid)
			

               # no = raw_input(u'输入投标金额（以百为单位）: 回车退出错误页面，0 当前价格重新提交 \r\n'.encode('gbk'))
               # if not no:
               #     hd = get_error_hwnd(threadid)
               #     if hd:
               #         click(hd, '00CA00D7')
               # else:
               #     if no != '0':
               #         no = str(int(no) * 100)
               #         SetText(e1, no)
               #         SetText(e2, no)
               #     click(a1, '0106023D')
               #     ac_hwnd = get_sure_hwnd(threadid)
               #     e = win32gui.FindWindowEx(ac_hwnd, None, "TEdit", None)
               #     sure_code = raw_input(u"校验码:".encode('gbk'))
               #     SetText(e, sure_code)
               #     if _test_env:
               #         click(ac_hwnd, '0095009C')
               #     else:
               #         click(ac_hwnd, '00A100AA')
            except Exception as e:
                print e
                pass

