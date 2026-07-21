import json

netscape_cookies = """# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.tiktok.com	TRUE	/	TRUE	0	tt_csrf_token	tBSC9dTk-JH35WBY99mSB6XLKDnV2BneKL9Y
.tiktok.com	TRUE	/	TRUE	1800170816	tt_chain_token	IxfEFSGhjGj6qtFTaD/pXA==
.www.tiktok.com	TRUE	/	TRUE	1810538816	tiktok_webapp_theme_source	auto
.www.tiktok.com	TRUE	/	TRUE	1810538816	tiktok_webapp_theme	light
.www.tiktok.com	TRUE	/	TRUE	1810528067	delay_guest_mode_vid	5
.tiktok.com	TRUE	/	TRUE	0	s_v_web_id	verify_mru7gg2b_a8gWoECq_lbq1_40nm_9Sew_ql14hF1SybHI
.tiktok.com	TRUE	/	FALSE	1800170811	store-idc	useast5
.tiktok.com	TRUE	/	FALSE	1800170811	store-country-code	us
.tiktok.com	TRUE	/	FALSE	1800170811	store-country-code-src	uid
.tiktok.com	TRUE	/	FALSE	1800170811	tt-target-idc	useast8
www.tiktok.com	FALSE	/	FALSE	1792394811	last_login_method	google
www.tiktok.com	FALSE	/	FALSE	1784697716	tt_ticket_guard_has_set_public_key	1
www.tiktok.com	FALSE	/	TRUE	0	csrf_session_id	3b160603aef2aa206c75c25bda2385b6
.tiktok.com	TRUE	/	TRUE	1789796162	passport_csrf_token	8aa20cef3f6210134cb0119223be7104
.tiktok.com	TRUE	/	TRUE	1789796162	passport_csrf_token_default	8aa20cef3f6210134cb0119223be7104
.tiktok.com	TRUE	/	TRUE	1815716162	sid_guard_tt_open	4908bcbbcad272ef8e6bdff8e6137b36%7C1784612161%7C5184000%7CSat%2C+19-Sep-2026+05%3A36%3A01+GMT
.tiktok.com	TRUE	/	TRUE	1789796162	uid_tt_tt_open	e874e64a7e86371bc568ffca0ec7569da6aaf3d446185fdd224aeed4e25a7060
.tiktok.com	TRUE	/	TRUE	1789796162	uid_tt_ss_tt_open	e874e64a7e86371bc568ffca0ec7569da6aaf3d446185fdd224aeed4e25a7060
.tiktok.com	TRUE	/	TRUE	1789796162	sid_tt_tt_open	4908bcbbcad272ef8e6bdff8e6137b36
.tiktok.com	TRUE	/	TRUE	1789796162	sessionid_tt_open	4908bcbbcad272ef8e6bdff8e6137b36
.tiktok.com	TRUE	/	TRUE	1789796162	sessionid_ss_tt_open	4908bcbbcad272ef8e6bdff8e6137b36
.tiktok.com	TRUE	/	TRUE	1789796162	tt_session_tlb_tag_tt_open	sttt%7C2%7CSQi8u8rScu-Oa9_45hN7Nv_________bt4mPp6Pk06KXGU9Wm4gd2OnG0yWmkEXRk9EeKzJ4Mqg%3D
.tiktok.com	TRUE	/	TRUE	1789796162	sid_ucp_v1_tt_open	1.0.1-KGNlZTZhYjNjZjA1YjZiODNkYjU0Y2RkNTg1ZWE0Y2ZhZDU1NDhkODcKGAiHiNCg1-uVr2oQwYr80gYYpxM4AUDrBxADGgNzZzEiIDQ5MDhiY2JiY2FkMjcyZWY4ZTZiZGZmOGU2MTM3YjM2Mk4KIIiMgaWd4mBSDjVSxzrjeAXW1rhXbQkSobEJNW5A6aVHEiBYQBRAEpenzGsfIb9F5_5iK-SgviMrRpUv24brJGefKxgBIgZ0aWt0b2s
.tiktok.com	TRUE	/	TRUE	1789796162	ssid_ucp_v1_tt_open	1.0.1-KGNlZTZhYjNjZjA1YjZiODNkYjU0Y2RkNTg1ZWE0Y2ZhZDU1NDhkODcKGAiHiNCg1-uVr2oQwYr80gYYpxM4AUDrBxADGgNzZzEiIDQ5MDhiY2JiY2FkMjcyZWY4ZTZiZGZmOGU2MTM3YjM2Mk4KIIiMgaWd4mBSDjVSxzrjeAXW1rhXbQkSobEJNW5A6aVHEiBYQBRAEpenzGsfIb9F5_5iK-SgviMrRpUv24brJGefKxgBIgZ0aWt0b2s
www.tiktok.com	FALSE	/	FALSE	1800168259	g_state	{"i_l":0,"i_ll":1784616259631,"i_b":"wm6b5ibIS/kL5DJ0YKeNdbCdIrrkf4gSA83fZVwdGX8","i_e":{"enable_itp_optimization":24},"i_et":1784616259631}
.tiktok.com	TRUE	/	TRUE	1789802811	multi_sids	7664833217329775629%3A81b9f165bbe6a11681ea56f2b0b2b661
.tiktok.com	TRUE	/	TRUE	1789802811	cmpl_token	AgQQAPNSF-RO0rpgG5T1vJ008D9sBe4Rv4zZYKZC6g
.tiktok.com	TRUE	/	FALSE	1787210811	passport_auth_status	e5dee0354f8901bd81b243ec987e76cf%2C1696553b7c234185192d854a0fe2dd49
.tiktok.com	TRUE	/	TRUE	1787210811	passport_auth_status_ss	e5dee0354f8901bd81b243ec987e76cf%2C1696553b7c234185192d854a0fe2dd49
.tiktok.com	TRUE	/	TRUE	1815722811	sid_guard	81b9f165bbe6a11681ea56f2b0b2b661%7C1784618811%7C15552000%7CSun%2C+17-Jan-2027+07%3A26%3A51+GMT
.tiktok.com	TRUE	/	TRUE	1800170811	uid_tt	c40eb592d5cee2d33de84cf22682d5871519151fa2987a52716d43a379e5105e
.tiktok.com	TRUE	/	TRUE	1800170811	uid_tt_ss	c40eb592d5cee2d33de84cf22682d5871519151fa2987a52716d43a379e5105e
.tiktok.com	TRUE	/	TRUE	1800170811	sid_tt	81b9f165bbe6a11681ea56f2b0b2b661
.tiktok.com	TRUE	/	TRUE	1800170811	sessionid	81b9f165bbe6a11681ea56f2b0b2b661
.tiktok.com	TRUE	/	TRUE	1800170811	sessionid_ss	81b9f165bbe6a11681ea56f2b0b2b661
.tiktok.com	TRUE	/	TRUE	1800170811	tt_session_tlb_tag	sttt%7C2%7CgbnxZbvmoRaB6lbysLK2Yf_________ezLp7csajdvo43JrV0kqfwq6IsKuNe5WeqtRQdPXBXWg%3D
.tiktok.com	TRUE	/	TRUE	1800170811	sid_ucp_v1	1.0.1-KDAxYjA2ZDZlNzkxZmFjMmVhMDRhY2E3YWI2OTQwZDAxMTE5YjViZGEKIQiNiLnst6a9r2oQu7780gYYswsgDDC66vvSBjgIQBJIBBAEGgd1c2Vhc3Q4IiA4MWI5ZjE2NWJiZTZhMTE2ODFlYTU2ZjJiMGIyYjY2MTJOCiANs7p2erSkLNPuPbhhnsrdRkuPg-805DiSI9Mt_1GLlhIgJ7G0m-fbViKIcNEnD6aSZvuWFoAbDhWeARIQUD0oy3UYAiIGdGlrdG9r
.tiktok.com	TRUE	/	TRUE	1800170811	ssid_ucp_v1	1.0.1-KDAxYjA2ZDZlNzkxZmFjMmVhMDRhY2E3YWI2OTQwZDAxMTE5YjViZGEKIQiNiLnst6a9r2oQu7780gYYswsgDDC66vvSBjgIQBJIBBAEGgd1c2Vhc3Q4IiA4MWI5ZjE2NWJiZTZhMTE2ODFlYTU2ZjJiMGIyYjY2MTJOCiANs7p2erSkLNPuPbhhnsrdRkuPg-805DiSI9Mt_1GLlhIgJ7G0m-fbViKIcNEnD6aSZvuWFoAbDhWeARIQUD0oy3UYAiIGdGlrdG9r
.tiktok.com	TRUE	/	FALSE	1816154819	tt-target-idc-sign	DODbbFaU5k0t-KwAhNyku4_azTd2adM__pNOMpmUK6usV3nuleam6x5qNqashoN75AiCV5AIr4RtZ7O9xYNPYgQPGwpdsDd1LcilipUQEVeUJoz3nJh4y0w9vC1FdlxSio2ae7TWL0hBTg9-_WuHNKWlA6s7RNQ-qSxCCJjNMrjB-1S611CB7LVauL-4j9ZiC0mG8tUe-goCSNFQ_3EUCeVcjdWG5arkBHUbJW7fNC1ZbvPX5qAIPomAbAYq1uLXWUEBizVq8HhK7EWszlMe413ukBFPzaTLnl2ht66QV5ZVZrfvGYNEDR8zdgvvKJGsDOcnZxzalJiUM1j5Pj3q1hZH4xNrGiulq09zYMiItbIsLTZMc13Fc8tvLNcpt8De5SlfdsjZn5rg5Rtk1X0zyn7RM3j5PNmo_ejj-BJ-0ZvgrNMfceFsdalpoTLlcACUp69PhP9luUXEUMDSm0h90s5K8bUXadGyPQYLa6JghDACsZ4B-eI2wIk-EbNxfnHZ
.www.tiktok.com	TRUE	/	FALSE	0	passport_fe_beating_status	true
.tiktok.com	TRUE	/	TRUE	1816154819	ttwid	1%7CRvQHaH2HIfv_kIpOYKLW6pdCF-J7_VKRhRr6u_jyygw%7C1784618818%7Ca231fd34306ff596115e38684e5b8a6bde38bd1a4bb9947eb756ebcb37bed00e
.tiktok.com	TRUE	/	FALSE	1816154820	odin_tt	b892a89bf1575425dffd66f2c65c648c8a2cb9ef4b0621c4cadffb841d98195b245fe3c20e55cf8fc09b6b4fed993bd16e58a1e43a93a0ae7aa39195b6ca906d48db013b53733287a1e4482577dc93fb
.www.tiktok.com	TRUE	/	TRUE	1785223621	perf_feed_cache	{%22expireTimestamp%22:1785222000000%2C%22itemIds%22:[%227643254805774765325%22%2C%227642981932233526548%22%2C%227645260472983358750%22]}
.tiktok.com	TRUE	/	FALSE	1800170811	store-country-sign	MEIEDIhhMv78vYigqapGMQQgcyNo8ZjdvfwX8sFS5kuOetmFwX5xByN-bFNpH7lo23oEEN4L5I5Ea0DphNYs9SM5sgw
www.tiktok.com	FALSE	/	FALSE	1792394882	msToken	KN5dv8POC8K6HlFDxLoGvuLNH83U2Zm2dJ1h7RU8wenZ3YvZa71CpXVc8myZ7JyBe1bmxgN3cOlP6_lZT7OSo_HMaWY4VKKvzY4ocKRQyoA9QymjMJAo-iaGk7JlOd_S_3MJBZI32mmen9wlDobZiABPK_oIbP85t451n1qu2GA=
.tiktok.com	TRUE	/	TRUE	1785482890	msToken	PfYC2kp82Uo-oBOGjGnVqG2c586sfhmwIpeeNHVB2Xb0FOv71mb4ePPVC7_zn2EjayXj88BzzlrAEaJf6MQChLQIYVswceD3mLDtPOKmgTnlPlTsVNMdacdYpwA91eJvMWzPuTyDupL6O5BBMBFbqUOpAMi_s6CQoH4Rfkjv1Rg=
"""

cookies = []
for line in netscape_cookies.split('\n'):
    if not line.strip() or line.startswith('#'):
        continue
    
    parts = line.split('\t')
    if len(parts) >= 7:
        domain = parts[0]
        # Some netscape formats omit the dot for exact domains, we keep it as is
        
        path = parts[2]
        secure = parts[3].upper() == 'TRUE'
        
        # Expiry: playwright expects -1 for session cookies instead of 0
        expires = int(parts[4])
        if expires == 0:
            expires = -1
            
        name = parts[5]
        value = parts[6].strip()
        
        cookies.append({
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
            "expires": expires,
            "httpOnly": False, # Netscape format doesn't explicitly store httpOnly, defaulting to false is usually fine for playwright injections unless specified
            "secure": secure,
            "sameSite": "Lax" # Default fallback
        })

output = {
    "cookies": cookies,
    "origins": []
}

with open("tiktok_auth_state.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Successfully converted {len(cookies)} cookies into tiktok_auth_state.json")
