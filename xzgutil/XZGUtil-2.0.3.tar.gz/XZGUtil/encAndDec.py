#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-05-31 9:52
# @Site    :
# @File    : encAndDec.py
# @Software: PyCharm
"""
加密和解密
"""
import hashlib
from binascii import a2b_hex
from Crypto.Cipher import AES
import base64

 # "
 # No module named ‘Crypto’:
 #                pip uninstall crypto pycryptodome
 #                pip install pycryptodome
 #

def data_decrypt(text: str, password: str, offset: bytes):
    """
    对数据解密并处理
    :return: 解密处理后的店铺信息列表
    demo:
        password = "w28Cz694s63kBYk4"
        offset = b"4kYBk36s496zC82w"
        data = "70BBF29AB4ECC64C1BA001A5095CC3232C1C66767D10C7506C76A01DE2059FCA714FAE55B77DB5BF7B29597C52D22B81EFF70D5D02BF108C2DC96B34E34AA43E6AF2B9FC4E5544991DD440485B5CC754CBF4DDAD9BFC3587E3DC480C2D328D1844B602ACE2EB2EBDB788FA8646B393D84CC9414FAD0647E816ECA8F57D786F991C18A83B8DF2756993A9CC8185DD22566ED19096E1BBA962733852D7DF666F38DFA9B6112072DABBF251FC348A5DBA0FC3A6321089ABDC78C1A2273E990873B39C30E91A1A9DE49FCFD6C542F049F94BF7AB6CE9400C2F50AED75FCDAF758BE00C48FCF11D4D6CADEBAF6BC48B5E3640929FABA481917A04B71F8D0626F513CACB18B28AB6EDF5B32C0106C7C3A6104EA32DCEF19B140A6C1B55DA19B472DC2612D18F2C9363347344621539E6DCFDA54A9E56C83F195E7538D7C88EF2504953EF31B739028E9412FF23D4FD9F5555DD367B703223836A22F556C8D924AF785513BBD562FFA32B23A41A91E32F8079333AFE509BB9C88F1D1E917171A13691A17D5CF4305BD9A2B95EB53BC5420C978A2BDE79EABA86116B7435E1FF2BE2D847E98BCFA95E3AAD7200EDF8D20ADBFE13A33CE3E69C433B46D4DE9083085D326CED1E8959E2A38F55E6E6D3AF157D5C1F7CE496AA85455B67FB18CB7AE0C474CB4E5419CEA859ED140AF7A2C5A7168ECCE994173EA2E1A1C6014574B5C100F43AF4551CFF1A10F355ED83BDD4B5E3EDD5FD631AC7BA41A5F35D4F86978CD1A214E88ADD1EBB717DCDEF65A45B90EA32D8A419C7C27973ACD0AEBFB7FB3E95CBBCFE1F2B140958FD031044ED0A3E442816455C86BC98C84130AA2CAEAB3F198D6B09ACA459A0A69111D97E3717900A8FD79D86FD5842819E23D27674C151F240FDAEA9093D17A65F0AD7631DF18B497AE4570155D9ED4D461FC1E7BB95BE990157C066BEA1A447D165E5040F3CFD8B4CF80122D048AE56DD6E39345A444822E0102BAC1606394B09F4A4CE968480190D92DBF758910BCCBB502058B21FB40D57ED7D85C27B3373BD4AE132CF6380C4DC53644A75893D8BE0450D0AE0F465C984D1E5D6CA18B682C943ECC96D16351FB60E3FDE8A96994463AB42B177ED4B14BE62B85EBF164FB3FCC04859A6C1D83AE23A8D39685016E45C61D1679018118BB7C71C572A5F529D5DCF8FB5F6DE20E86114EF204FB100EEA8B53D449E44197728989C45F5B09496008206BF9827523AA731FE988930A4DCA8449F89B34CF8699694F51A876A057F3FCB6FDC9466E934920043269BA41626356BD61847DF06BCDB6C277F0C0E3B5FA8B087C1769C02839F017F34961C6C364D2DC15AA2888E9492ADABAC0F54C534462BA4EEE7CA7EB9451DF148F8A7CB7CD37F3D3647674E985D0448596827A5546088FABD7A1739BABEF0075DDAF26936EBEBED54D18C34D22A889EF3CE5A9E1D886F3BED2FB3E5745F5776EA926B715A8CB2387F9801A528D0B7221C1A757DA9A863B0236AA986AE67572F0DD3D053E29107011660A663D8C3EDAB1D78819445C569F00DECE79AABD381BABEDFF798F6D7FA9B7752A9B1223DA8BA118A680F4389B18F3E658A664170C1E21E73DB59160C231EDA1393FCEF45C87D8CE3EC046C1607D8358C4C8F0ED75927B0E08CC254FBC6AE7A7D8E09780D5B9B1EA285F95E9433F5BF367DFD7A6D2629A79B5B7CDCE8E6F02EED4FEB99438C058184CA2B07768EB9D6D06A8DF8EA140268C0B9F5FEB0FB4C160554226FE2C1D50212EBF9FCD74220D72E2A649093D2FD5E64601A68AFCC8DD6F5AD6785C4604F44F1AFE0C1CAACD2DB01B82A8FFC90BE19449082CEDD62019E8B82DB054396CA564F7D78C32C0C45267DAA23782D39FB213A9F2C28E0EA86F751C25D8BE3899E02C682334AFFEBD8663C3D28F147426AA8990831C01D758F95720DC1469A03C074D035A7C23ED050E9B28127F5FA1FE385C7E34A9FDA775C899C395F5DB507A2BC705E1A351D799DA38372DA28DB54F320F28DC2AC049E5064DA0FD4524F657859CAC76DE7DF576A541E25907CED43574CDC6718B8A35EDD5D0D6AED8B0B3A3B26224BF8C4398710C3B615641EDA4C3132EE4B76FC37035B228D6A40A5A8AB8A3340189A588044F743DFE0D788039043FFA8A561D68738BCEDFBB5C52F1570641633F5ED5311533717200900F6057AAD04C8C902D4E5EA83E849A30BF3862592BACACE064E4E5B7CEB5DD23EB1CBBC97D635023C5B9D554A33CB62F99663F9B98C8E409B659BB56FAEA2AEA642EE5C32F3AFDB7FF941A961833858EBB800281B1D1044903AF76AA128C268A78D70AD085F22D1C0AA9EDBFC2CC719E132DEEA0565BB70AB798F15AF0BAC1E819964374CED826A10D0F958596FF1323E55BFE36E7EAC118CB57085C15F2334A3685FD5536609225D52203D9261CCBE811A20C2DA296446C2CBE199D3C3FC32CEA00AF9443BFD5D50E7A333DC98C45CA61A909D600839F04CE8CEBA0D040C21D6AA4F4CE816B9E5936D1C8825A48C81752E893C9CDBDD09ACEF170EE97FFB676923013DFDB2C3CDC5A1DC442E9FD7EBCC6C377170A3AC01907A23DCB34DB25802E8466BBE2895EE99405570CF164C84EEB733C1DEF53303F6436836B1E26785936F4BC1B021E7EFC4FCF1166EFACDE4B1D7B0F664A7E7E40E963222485EA98C076EAB1D35646ACD19B38E26159B271B4794928C67CD4A5559C4AC4AAFBC3A09AE79FE677F21864A6DBA9FA2BC24ED44E11753CEC7DE17111F7BB0EB33787A2BEE50FDE12ACBF428D91B59D2ADB6F4E579299D5285B320D97895A9B2933421ED0E96EFB0FFB13F3E2035885BBE6C29C87295CAECF5D129105F0D5B5A056A462E0F53ADB593E51AE0AB108204E83636661BF7C603514BB96D95A09F975F50D288AA9D16E511BE77FF33CEECFB2EEAF87CA170971D9E70748EFAE54103F57C629971ADF514971285A955F22536F81644E1470583967CB2CB52A7A82F00F1E07DBDBA280D87E3DA9B912D70648AEAE2C1CE80CE620D0E3799841866FE074446C35A8AE1223E89C5FB7D7265A8E9CD88D1C9A846B790247EA22BDA24CA2E4AB1BF7B209B9888CDB7D6802551E77DF3E684EF0B9B9BF7F7FFDF9F85FDBA20A4EFE88B1C2E3F178F8E83402719E2DFF3B00C3F9076AEB0ACA777567DC4EA2CFD2C486C7D9307913846883FAFA1777FA172B8CAE573B2688932D02EA3AADAF11C4DAA4B5AABBC31CA68E90E8E0C31FBF9B978C37D3ED5BBA97A8C41831BAAF7013A162ADD13A25BA813FF52F51540CA3927C7624CD545BD8C2637155DD3495AE4750FE667EFE85FFCAE129DC709CC0606A0237EE4A68C26C7D3EDBA6358F37F62482B54477D70849F3A7D1F56F8C1546F7B654962908D04F39D1922333A1F8DBF146ADE19F4327BA2B28A84DAB4A58C6C95BE6CE5D827CE6473010807D2C317E4AA328E0BF2657D123D262A9A9291988D46F332F06DE0D42FA206FEF660205DD5E650C4AE8C1B4C378E61BED61F8A11EFFC9288484DDFB245229E1CEFB82848942BC8247DA219ADA8812C96F9E8EA0713B29B05D7AE42C39B1E4805FE3B09361B5FE7ACCCFE5A73293D6A74DDF7DF8C59A9E70D6870D3B5FD18FFF886B6E136D29D309BD794CFA8F56FD1F6049EE3A164A9805955C1CD408DBA1C766E42D92025AA8853D96E46170A92BC4BBFC42FCF1B426A2123B8EBE261676C7DFBE0E7CCCA788CECFB78BAEFC0BBD92B82C2900DFFB82CBDE56C6C4775B65475647A6AD223F2536C4A6BA6524BC738542783E7F3934EDF083E8E77452716B3AE18549C2256D18294FC55B6908813F352EB3441AD5E2445165853DDB8D61FD3536D6328413ECAECB1005BCC3FD003EFC796CB26D21905D4038A9DDD6F211954F0C9B58AEFE74CFA79E938DADA88FEDAFDD546DBE07D86D104C0F78C4FBC4F345773939F114D46B27C4F23C5F1AA0CB92456C4AE79F1AF2A52219C8331AFFD1BB14E2DCBB2261ED9FAF4AB95F7AC35260E168D76748CDA3D18906097E938621186405FD044F8EEA7D83A9C74AC336186EBBB5947498BE5FBEECAF52298472E086601B194B549AD029E2A196AB9B93CD7C812EC007F46C8FA9703A9BD8E5144C2E1EACB7D9F97524AB7E8977CA4D72A9AE1543A71ECDC2EA3CCFCC60BAAD335053529A19259E942B9437AB5424C58612C78C782693757A34120FD21B9B0E28B56D24AC975D3148B91C9E0D6BC91B2FB96A9EB6160F86DAF81AB6621D62624E8F1AC88D96E1C571578BDE7698A53A41B55F63DA9F7F9C11E4182BC317A837ECD64AF85BABE699F901DC67DA4025507DB404A75AEC0D633EEABDEDD34C9934D8E162B0EEC44674E8619BE583961697497E4F989A87B8C918BFC313C2C96439E9347A3828DADF9E11AAF8A7B6F9E704DEBF76D959413DBCDF2D52D1C2F0952D6382F625782F299D85DAB03A60847414043DE7431B5B5C02FA4B84BED7834624D3ED5F65621D99B3F592EDB52AD6C0803D17AED89AB66DCC4B4D8F6CCC5DF183FD76366D56315FDA09CC1866E6E0251B6346826312F7D7236FCAC7FB1EF272B125FDFCAACEB3E2A3A38DB0B62ACDEF373CCBBDCB8E3F10A5646C487662E2A241180142D3370BEC7571641F660F33C32A4CC534706325B19CE33244EBDE3C4DB4574B6A87C2677AEE9B3249F0C0DEFB14921C7DF168CC5DC42F3136ACD07944B564670E5E172258A92DDE64E514E940F22957AC762221CB8F977B61EC3C2CD69ADC6317C993C9128971C28CB18CDA94FF050313652835DF97BDF78884E5D295DBBD049D5E8A87D87B7FF9B98C0D2CC7C0CE1CA0C95ACD10B0EB8570E3C0965BF22E0BEDE7475557FDC549197927C0DEF8C6AA90AF0025B8B42D46801FDF8A13694F38514C1DFEB3E3FB1B30945060667885E16DFE5448DE32FAAE1683D4C62D55B247F7160AC6D3483107E374EFC32FDA04CC2052D62CEEA3F9849D699D7015F690EA201C64D79918183D3FCFF9E5738D263EA9709ED7D9527D8A1BF2A9DF7C5CBA8A38F5856A54BFE629EE9E2E4774FDF41C134430201AEE941DA34D2DF80D7788245AE5CE88074BF17656138494292A8CD72FA6496AE31B53B900B0AE5DAF19FA175EEE915ED4227E06E6FBF32B52D26F2A678BC4C9B6755C91B8CF5FBEB8A0854A80D8E051AB8CECC5640F74B885A120CA2961D8BD41FA6A0674FA1E67B46DE13BC089CBD8B04972F855DF43D96E578B7F1D1FC14E5E06D3BBFEFF1B8AB4434967FA61ADF2582776479FE8C80F13A73334EDDFAA2E24BCDB04AA8BF3809C7C4C09DA8D81964B5141227A9715F128F7D214A1F50B50DF68884F288FBD482F727CC58E8F21B17928D4FE626932DB26986D7F63BF782AAAA223300662991E5E998CB88D4FAE17D62067C7EF8703E08514A993038DD7F437E1AA4983C45EF6E1D082C72A671E7C6C241BF73CEDA7D191565BABF54EDE5067898A3756F3C7EF97D2B5517C4CCB63273D9259CA644C94C4CA9F46E0074139F2187DE2F980D970697291F1FE8515D03ADB5E90CD91CF9544B3B9E5DD4D02616FF19851A6116FD83850BE52291DA7017C60C31132E338D03F74A6CFE584E123D6C4D3FF66DD2AC3029E141B710526B10F8EF9F657E2F4EBDA6FD94D1137ED0FC73A6E343CC8A9474FB0BE5695CFE8CAE3F811FDDF625C9EEE22BD2C67910B88A33214CC1C75111B53E3AD52E3146D539AF5E6538A552BED62622BCAFBADBAE36B4F21B13EF30814E53DF40A5B3A841C8B36ACEA8279E2E13B1295ECE91A0382C7D662EB587453A9643E4A61007A59C079BE0DD06EA0571A6B5C782F1A011716159397D4936846E4790DF147717EFD5680ECDE0A55690CE6C3A20DE31D3DFC82A4C3A5EB24392FA04F3957E1A8BE88EB4916B3CBF2A6E736046740E1F1324E8AF5562A6D6673A1A686AF939807F9E6E401A5DC9BB30694BD4E17F7E8651737B98B8057F8CA29353F5CEA7AA4B2337F8F5FB4D2AD8A490E0533EE27455EFBE397E530A8286AA9311B66AEE845F8F46DE7FB446614BF82CD6031098D34B9F2162472EF86F16391EAC646808D47D4F3F920CC7C459402A77C2EFD529C382181E0DC67ED6C1D78AB8D0835F1E977511FB8F3DAFF1F23C6F71BCBA1B5D463D544FD4DE0B2598791FF6CEC012B875D7AF878EA064C3283C3AFC46D83FD33E706B9EB2AA25D945A3EAF2D3EE772CF0AD09423D225E805EF83C6455C2B9AC238D1BFB93BFA7674682B7B2FE469A150F27D51BDBE86215C272F626C49994652B9DE4178980798990E37261E7D434AB804E87A617736DD9967A4A2427DB5410699577479FB78FB1966278A7BEC8ABC9FBB2CDDA699E868421267730E8DC49804544F64EB0DC17638D2E2E5DD13ABFF798EE5D99F8B1116D6EF7BA9FE5D1B9A8F1253920553365D6CE293ED4594AA11568F2584CE54627F50316C16DD93DCB27DBA6E57DCB24387725B1CD9203F405D0663D0B4E15DB778DCFFEF35A7A895FE91253F10728780C83B8777AFF6BFEB2A8C923E0A7DE0D68958CAAA38888B5C8A21C76E82361C9864865A12C4286406A68DC6E3693F219F210EC2C43781181FBB4309B3AC5BE17FD5E90DDD9130AC05DD6767F4DC68B40ADA17A46A696583B9805603461624B7B27AB9084505044C6082F4DBF0A10B8475413E46633CD06CA6BC4633E5A0C30A54E731845F7C7EAE6EEDC13444DE5C758DAFB6E132029BB430E3E17EC2D6516B55DEBB6A8911B2034CB287997F11B89DABFA3417FDB72D51EA8A8D89FD704E231C627E260EA56A37C5437878157F5B82E9C4F930E021D6F5A7E0595DFDA01F9250717E083F7093BBA8CCCEFB9F61E1EC2CE045FF7261F260CF62331EE456F66BBC03AEFA9C9554D17CFBCA71B0E016D261DF2FD975D4B2B85C84546255393FC33E74ED0A35E63655C03832E223E1FA2189A5B176E0D6997FB28ABE89F7A5DE089EBF7535A5F4FDEA4E53FCC9985B16ABB34EB5CB6038958ABFA9D45499BD91707E46FBCF7A282E10498B1662CBED8B5DE5E4B9380E9164BF073EF900EC10960F3CC8DC46E2CE2BADB69A3D561EC95DEB813524ECE15D12C1CBF16CE8BA19E2CE9D8389EF518BF65CB5C2C81BC496641FEAB3F391B87B7D841BF814FB6F1E13EC9EA86CA0F4EF9DA8B5E9A1B3BB34EA1FA9F88211C289F66E5DA3AAA0AD9FD325E2C7C342A3E58F421F2A9DCB3529F0852050F0714DC9F23D7CC3934AF8210E556D2636869AB9243DFA4A7855B2FBE0A8139AAD6143BD5DBE5FD14E20B0D0A28F1C0EF644C37475A36AD1F40E7EF846B36A110CAB5C31C6EAB919AE98AC67BE25EAD575274B785B37B9476AFE849C6119D05843450E0584F17118BEDE7D3EE6279A486143B21EBB7C4AA0041849580ACC7D3ACEF9C959076CB81C239E2C60B0FF81A057AAFC59603016E01A14D24A20D481099857D402A0D8B1B0E14355E8A76BB654202D4693C3DD418D8E20C0E9832B7B4EBE507C21096EAE61161FD11AD62D2137AE860CAC33FB82544EE794273BD510C5C0DFE7423BB4BBBFBACFE8ED1830DB95C2378C3BE7F64FFBA57352F7E8783D4AB2DD524CED98AA7BA280A164F109F5252490429BBABA5E359DB3A3DE3121CAF9F1CD5841A90A77A468D09637E05C883C0ACD7537DD66B27973FFC81D49172993F8B8BE7D0718AD0FBA43879247E2589371EF1246C3D863738B6FAFE1F0B7E2AEFD58A99FC85850408B25F19F70BE285F4D085DA136631921C45729A1DB809889120439C9FE84870E94EB9D7E2C5F34DFAB322682D88054B9A98EF343219436D51C5C968E7F1BFE24CAA1CA915082EE237480686A97C07FD27D1621E3C4C6E2237A473405E5FF63D7A83A8B8F747434886DDBD99AFC898B6627128339FCC74F084069BD6ACDA3B713FBA734E69B01E9F47DC2A75942C36C699000E93D4A952FD39CB42A23151E637B7E60B2C0E5DDCFC2D83B62D417C09ACA6FA221D5C1D0AA6D0E0FE330BB89B031483B61F74FFE032BE9B1692A09C60BE051CF05D995A93882CE15BA13E8B85E4B7AA61D6370E7270CDCAA2EDC01FB27F06D536D007000BB84A36F8245B8772ED70A4FD63749625F73D45F3062D1CB2A1CAA223FB60A847E8BF555D5DE31402A715C3039AF179E674E63EC257DE7AB8C1D3CBE7C4A71F4F8EB58D3084340AD2AC65EA008767673801B87B415F7F13019EC2BDA36DC8C809AC6BB6B24F2B2CEC67544FDFF27333DA5E0169C8F2A4208FC8D47795A6298DB8FD433B8B492DB126352542BC7A034500371A15BC4B30D68CF10059A2390E047436BB56F968723BB3DA25221B1484421D8112CA5E9F5847E56E5AA003FFF23CC56C01A8BD93900AE9232DCCCA794DCA055CEBB4089697B2BAC100BF412356DD82E88C45355D6B0C3E06F73102990CAE14BFC7E90106CDE6D7F3EA755158B316C972C2CDE3524D4D3F920F777B2EAA036A6D4820D0EA0CB8595ACB624247C3349BC79DA323A5D93A6C4956BFCB3FBE4A6DAB7A4BAE33AEFAF3B7989C886B28AF8BAF8A33E3FDC021AF1E3312511CE1E3FAA15A3FFC4F59F2EE0923FBDE1EDA68B9AC295BCA7FE9ECCA92957BB0229B89C0EA4326C8FC9165486308481C07F9EA7FE83A0E0209807DA3772A26F8325C97E3B8F6FC3E0A3F7FFC1C3CC0CCB50FB1450253E56E582785C552B9F14D12D0863BC9E47360951A6AEE9130EEE67EBD795460E62CD30F6A0E496CE9FA60DED178113B6C59D6385FA221BB21CC50DEBE00B16E88EACE4E0B7679ACDD3AB31864B7DB3539B16A9B5E402AB672468933666FE2AE1AA7C220736412B55A2F5B2965F269E894C535075F6CC822B7D95C4E41C472A251CE4BDA5079DEFC2AEC5C774336786704F21505813EDCC2B758F6BA49228E5988963B25135069B2A027A7AA7BC926F3C2D501B6DE9590E9550C42D99D9BD42117000FD77232A4068B0FA0F95D01873D5534FB87B028844E5FCBD43805D7109E837DFC384740597475D2CD13302A00F4F42B2CAFC771A6C76542165B39500BBBB4CE1D4EE66E5193F45907D135197811252C9A52CE95C3B49E92B7D95D8767A00998CC90EF422E2DF78CEDB60D88FAA535F7D674B71143B6586B5CDF346424D5A6B96E9F011DABDDF00524025D5FEC830ABE42B4508CCDDCA2C2B9A767415E9B21605EFC39077B7C9C0FD88F5BE1C1B095D99984B25BCFBCA163ADB812E7055B4A35A8942CF091E7D91C10E132271BEF5D6109EDE54B7FB12CFC563A2BE18F083EDCCF8F59C9E50D3BB82F4DFA997E2108EF2CE8CAF4D9CC6E97BC6D74B2A1980D5B95F1F956082A011DA17BC85EB279EC96C4E5758C3D6635B389D0F30299CD29E04D0B21E24B8A2EFBD4CD95157E3289F523807B533CBFC727C52E8BF41A888477DC67491A213BF857DCF1ACFC0EF730D4D22D3497ED190A9CAF5643BB4612C9D11FA51938FAF7A024EAF177D72DC4016E0CE7B360F16E6856D81BA0E3B74CBA54F0F3C2823FA2EE20E226E381B1B0F24CBFBD3EC9AE7BFAE85DD38E1705F7159B5D4D1E6A93C7D597C9AF45FCE169A94EB8D71845C4E87FD309F283E97038E03C1F281D8CE81B19D010E3DF79BF03F84A7F106659D1CE459B4FA1004C68239595C8C2D77FE18BB5F7E9DC7DF913735F2761BD74D6D8A7633469AC70FEA27CAE61B6233B78869B2182E4BD33D8DEF564FB6E6D966BC0308903A65B02F4FAADBE1D0E56BF5AFFA4B5EBE9736714AE52C9D96E7704761C0EE28DF1EFDBC3230E92BFBCD67459D1BEF393F3810410E3DC3BC4A20A538291B9CB879290120DFD4D3D7815260E8B39B7CA93A40E02FDFCB4C39097A5CD6901CB51831D77E2F668477056A53751B19E54914A8B21AC2F6F6D3E8A85E9C4CE131D156EB400DDD8E15A04BB46DFD1B269A0F669A27F305CF0259B4209AE60BDA7C4F334A4020EFFA35F312B0CFE8748AB69BC312EB79827CA1C210B9C3B8D6193E06D0A614EC2DCAF7C9B880D2D29AE908449F98F360501782DD2865A203806680ED14BFAA6AD80A3BC7FBEC7B47DF2319527FD7B91B6F456CA45302949CC58469539D75FF939D627CBDF16EFD7BC5A4CDABDEEAFB1644B3B49C67D269A438F6C1C844DAF103AEE30C1763BC411E1B0B48EB682EFB66CE1ADA0EE09F52E05D0AD2F296C85B99E431A4B2448C604599E0050E718926B1FD6B27F1F4DFB192172620800919E5454992FADF8851911F7669E9870D559C8881E6E4F891EAEF682B215945D98DB3179ED197F00950DE9EB591A06D9925F0F5F596F71415A9D2E7D9DC739053EF42CB0FF84A9F81C71B4A551EC8B998522DF9ED6D6B144FDCC3C9B752258DC637AD03631D25EA9E2C2BF0A27D07B7B26484947AC2ADF14AF679677C91C68DE66309BD9103D6689087900723B733359A5D2379B106A69BDD83B9BDEBAD4EA19EF781B3CC02E39AC51769CD5088A94324898E28B6873B9241C2D65B484993D4123780F0558C523754DA1A18C168600410C9AE372DB8ACCE359E9D04C05670151A701F0FDD1F60F201790684622775725EED09F37B17F57C41FA7DA6D0E9ECB37C7D4CD78237E4B25EF1E034068C02AA1C51B61E012D294B1DF5E43AD73E4B08E67DB3783E832E9A0824C311FA2F9AAAC5964939BD109FD56CC91F13C89E760A6F241F6AD1149A0FC552F56B85A0181821D4CE7B41EC80EABF515883C2D2D34CA5B51B0E7288DF511F65E6F97C87F1AB603D6BAFE3FAC2E07434DFC8D4CF983FDBCB08163EA112D9BB95312F63F4A72471D9457C536F6975C8DB796A88782B792119779FC170DEF6853C47367091C42C05732EAF3B87CA24F9649E6F514FF053D521AB1985CDDA85D6071C450CC3D7E24D2D817B76276052C6530065B34F91D4266221B5A6C84CBFDC296EB4B8F607F6BB1A48C550E6A7C2E61600E95F7B9FA86F8B116B11DC5B9FBA14F8EA701CD5CBE7445E7FEA2C709E969D07D15861B32E96FF92A624B414A588BF179539AB6A1BB0CE490D315E7A4B191D728705859B156FF787CFAE49226A0BCB184843C2244E32979FD1148FA9C6C42D8B6405FEDD9636D1154C7177867296D6AA38D6B64C965D0F291252192714BB6545936DF12234DC14DF5DF5AAA1890CD97C74F5BEFCA0BE73B93D2F75A5B298F25BA337D02F02501B36E4C73805E6B160457922497416403D9B8584813DA853ABAE8E270C079DAE42F59219BE19F3290DA94709B2CCCF48D43E56A7AAFEEE46B9D498ACA79376194048705EBBEE94D35BB22CB14D530CA72A687EDD9CAAC8A30CC69355673E9BD2D0B79B2F6477E21D33412030F04548DFBB5D934A443A6C7502909E56EA9A0A5635B3B6ECDED26ECC60A801ADD97B0C6706F9F7CDCC9B17D9359C16F7E44EAF6883FE55FD5AC6E2F4AD585AD5650A2A671AEA046D8459E547B963A29EB44760077C44253AEE88A53067822D6F2CCD826890B1BDAAA2212AB8555101B6D91925313E63D386A7D787243E5681CE336C106FB16276EB9B655D5865CB390A906111443F5C38C2446F6CD807E5567FD7E5F4384AAC3605A5D76578FD1F2047ED3334CFDBE332A07BAADC9175A277EFF07481658B681125F147663B971E0360B2E6D5741F8BA7AA7E9590C4A772D08A1F664253009431A161E2EB317190D198620F82FF8592C7C8A5D0C57B96193AE7C651578A34EA705AE3A0B815D1439082FA125188A93E5832150246FCA12589C53EBA3C9E8BBD56AE98F846768E6771DD732A79D468D3CBE8A31931C917B3F74347ADFD445F03AD8FA66DA9C947B27DA5E7A2769386ACA7952A90316A4994FDF75308BD529A0D31045784E04E05DA1DA94EC64723236779F86FC713597BC038879933F15FA93EA5C651F8BC7B4C073DF30EC403226768961F3346D1E239EF8AFF24D2998AF1F65CF1EE2ABADD3C9FAF3BEA5D97A6EE459CB0F19E663DACB57ABC14ACC17AC202A5EFAF03854E1573AD6CCA1E2D9DF5A55C6DF968C5A9E935687BDF191966A60F1CD9B1B8EA404B2F06FF3350631CFC2CF54E11405B3797C0D8DC42B5856C1B75FCA6271C8DA35521C87B3BFF5C4723FCAA560D8E8E5C5327B538C1E2BFA5262E41DFC6F33F246ECB0579B0CD9145C65EA93666E85F9B232B29DEA02E8842591D5E9AE4AAFAE464C4D40DEE17516760096FC5864C686510E3C0369D60305AB758CA846654EB5FB9F7EFE0F04D0D6A726D7A85CD629BE0B8CA2B01E60421371D2297F2BCB3D6DEF0AB34B469CD1A117457177BBABCAEB7F47BA6261C9DB8928E5BF4223812AF63D23099F85EC6BC4C123A35B5C6F966C56AB5DA5917758829020AC77B803F766638312782514AD1CAAF874EC8A6FC3815F885BB08E21141602C3B3E03CB8E1703BD495DC1CF38A3A2D40E4BB104FDB06171653B62909834FAE11DD063123C0A2EB231183A21E3B058772A78D4FFF057A2BB3E0DCA9A72F8ED5E7502CAB504FB379D46E6C0B8898B6D346FC22BACA34652DFF0C342C20E9952A62255A3195FAF0CC4FB5FBB16E139C183F9A6E18E8A46D20177416407FE65286AFE7A85C4C62225B660911B5261BCFED4612B49AB8B8FAE0894A1F5FA42A9447EFBCB9D4EFBB8B0E39428F58972DF9CE61488D862B6E67D8CCE90B8050B19E5DC3DEF2716222BDC821EFE2945FB5B1BCFCC49B31E4D6BDE78DD5C1F31AB976204F1F49BAED8790AC777AB0E1A4F1D77DA1AFAE1FACFD39F7CAD1337A65C6055E1D6791AA57681E2DE10897D9BD5515448CC162007FCB5F6F4C44BC05EC93E5F84317DEECEA2EE5F99DAADF820301DBAD02865CF09C067F886885F59C28E76B263FCCEC2DBB5D0ABF357FA4906188B562C2DF75B140A7C9A820E48A12C028FF741A3323ED2EDDDFA6DE332BDD53D3950925FE648D36552615A1D0E56A4204F0B4C8283800AE8C7A5E48D5A37A6C754FBE2EF180D9BB71B2F8ADA8DB02E6D873ED178707B98D0F7D4DCEA64D767AA2339D4F1AF9C09C769C54DE8C8A631DF718DF481383E74F6F012872AEF9A1033433CC0165213717281F940B4C58996138E3B1D8B11E95F6759214D23A0213AC2FA907796C2A3A132350B67052A4A13417A5937A974BC369C5E5273FC8146DFFD7A3B0494CD2DC6CDC72668523C7DA0EFCBDAA760CB75E801AD65A999093354EAA0B6C07FFC82AB4C375C438CCDBD3A061D40D95F939992C6B4632D593758BE217ACE25D8104768BB8EF21CF5F54439BCE65AA98CBB4CEC841351F9D4441D3535B09692062A2D5BA5F597BC2BC44EAEC60AE0EBC03E4D91FE855288545415A132EC82186A11272ABD38803F39C52FE35561DAC770D6DA4F32BC13CA6914DF5123AC3D74232FA6C8ECEDE45A5AC9FCAA2F5FA9AEFC3E1FB640F322D6F73F088A4373A3E8C78CC70646D2DBF390835B6BC19543B23006B2280A8C9B1CE4C8B58D294B57FA414731C6CBF6DF356ABD4B28D4198D5302849401A836A9B9D2AC5F26023CE613621122CCDD6FEBC3C60A665AF8B768A32F12A62C1C494414FE0AA03B5D06B026F1F5E5729AACEC56980AD09B1F41147E0A7AF9B2BC86FEB4DF1503C85DFC8C1C157EE8469EC3CA1237E9C8D4C0E"
        res = data_decrypt(data, password, offset)
        print(res)
    """
    key = password.encode("utf-8")
    mode = AES.MODE_CBC
    b_data = bytes(text, encoding="utf-8")
    print(b_data)
    cryptor = AES.new(key, mode, offset)  # 偏移量
    plain_text = cryptor.decrypt(a2b_hex(b_data))
    result_data = bytes.decode(plain_text).rstrip("\0")
    return result_data


def get_md5_str(md5str):
    """字符串md5"""
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    md5 = m1.hexdigest()
    return md5


class aescrypt():
    """
    demo:
        pr = aescrypt('12345','ECB','','gbk')
        en_text = pr.aesencrypt('好好学习')
        print('密文:',en_text)
        print('明文:',pr.aesdecrypt(en_text))
    """
    def __init__(self, key, model, iv, encode_):
        self.encode_ = encode_
        self.model = {'ECB': AES.MODE_ECB, 'CBC': AES.MODE_CBC}[model]
        self.key = self.add_16(key)
        if model == 'ECB':
            self.aes = AES.new(self.key, self.model)  # 创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key, self.model, iv)  # 创建一个aes对象
        # 这里的密钥长度必须是16、24或32，目前16位的就够用了

    def add_16(self, par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()

    def aesdecrypt(self, text):
        text = base64.decodebytes(text.encode(self.encode_))
        self.decrypt_text = self.aes.decrypt(text)
        return self.decrypt_text.decode(self.encode_).strip('\0')


if __name__ == '__main__':
    pr = aescrypt('12345', 'ECB', '123456', 'gbk')
    en_text = pr.aesencrypt('好好学习')
    print('密文:', en_text)
    print('明文:', pr.aesdecrypt(en_text))
