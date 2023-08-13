
try:
    import httpx
    from colorama import Fore
    from bs4 import BeautifulSoup
    from os import name, system
    import pydirbuster
    import nmap3
    import dns
    from dns import resolver 
    import virustotal_python
    from pprint import pprint
    import socket
    def clear_page():
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")
    clear_page()
    print(Fore.GREEN + """
    ██╗░░░██╗██████╗░░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗
    ██║░░░██║██╔══██╗██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝
    ██║░░░██║██║░░██║██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░
    ██║░░░██║██║░░██║██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░
    ╚██████╔╝██████╔╝╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗
    ░╚═════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝

    Github   : Github.com/Symbolexe/
    Telegram : T.Me/Symbolexe

    """)
    print(Fore.RED + "[-] " + Fore.WHITE + "Remember, Run This Program with Root - sudo python3 UDCheck.py")
    print(Fore.WHITE + "This tool automates these things :")
    print(Fore.BLUE + """
    1.Checking File & Directory
    2.Checking Internal & External JS File
    3.Checking WAF
    4.Checking Subdomain
    5.Checking DNS
    6.Checking on VirusTotal.com Website
    7.Checking on Shodan.io Website
    """)
    def checking():
        check = httpx.get(final, follow_redirects=True)
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Good News, Your Target is alive")
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking File and Directory")

        webbuster = pydirbuster.Pybuster(url=final+"/",wordfile="wordlist.txt")

        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking JS Files")
        def page_javaScript(page_html):
            all_script_tags = page_html.find_all("script")
            external_js = list(filter(lambda script:script.has_attr("src"), all_script_tags))
            internal_js = list(filter(lambda script: not script.has_attr("src"), all_script_tags))
            print(Fore.GREEN + "[+] " + Fore.WHITE + f"{response.url} page has {len(external_js)} External JS Files")
            print(Fore.GREEN + "[+] " + Fore.WHITE + f"{response.url} page has {len(internal_js)} Internal JS  Code")
            with open("internal_script.js", "w") as file:
                for index, js_code in enumerate(internal_js):
                    file.write(f"\n  //{index+1} script\n")
                    file.write(js_code.string)
            with open("external_script.txt", "w") as file:
                for index, script_tag in enumerate(external_js):
                    file.write(f"{script_tag.get('src')} \n")
                    print(index+1,"--------->", script_tag.get("src"))
        url = final
        response = httpx.get(url)
        page_html = BeautifulSoup(response.text, 'html.parser')
        page_javaScript(page_html)

        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking WAF ( Web Application Firewall )")
        nmap = nmap3.Nmap()
        detect_waf = nmap.nmap_version_detection(final,args="--script http-waf-detect")
        finger_waf = nmap.nmap_version_detection(final,args="--script=http-waf-fingerprint")
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Detect WAF :")
        print(detect_waf)
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Fingerprint WAF :")
        print(finger_waf)

        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking Subdomains")
        file = open("subdomains.txt")
        content = file.read()
        subdomains = content.splitlines()
        discovered_subdomains = []
        for subdomain in subdomains:
            url = f"{over}://{subdomain}.{site}"
            try:
                httpx.get(url)
            except:
                pass
            else:
                print(Fore.GREEN + "[+] " + Fore.WHITE + "Discovered subdomain: ", Fore.YELLOW + url)
                discovered_subdomains.append(url)
                with open("discovered_subdomains.txt", "w") as f:
                    for subdomain in discovered_subdomains:
                        print(subdomain, file=f)

        print(Fore.GREEN + "[+] " + Fore.WHITE + "DNS Lookup")
        result_mx = dns.resolver.query(site, 'MX')
        for mx in result_mx:
            print(mx.to_text())
        result_ns = dns.resolver.query(site, 'NS')
        for ns in result_ns:
            print(ns.to_text())
        result_a = dns.resolver.query(site, 'A')
        for a in result_a:
            print(a.to_text())

        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking on VirusTotal")
        domain = site
        VR_API = input(Fore.GREEN + "[+] " + Fore.WHITE + "Your VirusTotal API? : ")
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Your VirusTotal API : " + Fore.CYAN + VR_API)
        with virustotal_python.Virustotal(VR_API) as vtotal:
            resp = vtotal.request(f"domains/{domain}")
            print(resp.data)

        print(Fore.GREEN + "[+] " + Fore.WHITE + "Checking on Shodan.io")
        import shodan
        from pprint import pprint
        API_KEY = input(Fore.GREEN + "[+] " + Fore.WHITE + "Your Shodan API? : ")
        api = shodan.Shodan(API_KEY)
        info = api.host(targetip)
        print(info)
    site = input(Fore.GREEN + "[+] " + Fore.WHITE + "Enter Your Target : ")
    over = input(Fore.GREEN + "[+] " + Fore.WHITE + "Your Target over HTTP or HTTPS? : ")
    site = site.replace("www.", "")
    site = site.replace("https://", "")
    site = site.replace("http://", "")
    over = over.replace("://", "")
    over = over.replace("://", "")
    over = over.replace("://", "")
    over = over.lower()
    final = over+"://"+site
    targetip = socket.gethostbyname(site)
    if (over == "http") or (over == "https"):
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Target     => " + Fore.RED + site)
        print(Fore.GREEN + "[+] " + Fore.WHITE + "Protocol   => " + Fore.RED + over)
        print(Fore.GREEN + "[+] " + Fore.WHITE + "IP address => " + Fore.RED + targetip)
        useit = input(Fore.GREEN + "[+] " + Fore.WHITE + "This is Your Target IP? [Y,n]")
        if (useit == "Y") or (useit == "y"):
            print(Fore.GREEN + "[+] " + Fore.WHITE + "Start Checking Your Target")
            checking()
        else:
            targetip = input(Fore.RED + "[-] " + Fore.WHITE + "Please give me your Target IP address : ")
            print(Fore.GREEN + "[+] " + Fore.WHITE + "Target     => " + Fore.RED + site)
            print(Fore.GREEN + "[+] " + Fore.WHITE + "Protocol   => " + Fore.RED + over)
            print(Fore.GREEN + "[+] " + Fore.WHITE + "IP address => " + Fore.RED + targetip)
            print(Fore.GREEN + "[+] " + Fore.WHITE + "Start Checking Your Target")
            checking()
    else:
        print(Fore.RED + "[-] " + Fore.WHITE + "Please give me a " + Fore.GREEN + "Valid " + Fore.WHITE + "Protocol and Start This Program again!")
        exit(0)
except Exception as e:
    print(Fore.RED + "[-] " + Fore.WHITE + "I Have This Error : " + Fore.YELLOW + str(e))
    pass
print(Fore.GREEN + "[+] " + Fore.WHITE + "I hope you are always happy =) - GoodBye.")