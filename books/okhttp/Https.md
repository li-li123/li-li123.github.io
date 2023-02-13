HTTPS
----

OkHttp试图平衡两个相互竞争的问题：

* **`Connectivity`** 连接到尽可能多的主机。 其中包括运行最新版本的`boringssl`的高级主机，以及运行旧版本的`OpenSSL`的过时主机。

* **`Security`** 连接的安全性。 这包括使用证书验证远程Web服务器，以及使用强密码交换的数据的私密性。

在协商与HTTPS服务器的连接时，`OkHttp`需要知道要提供哪些`TLS`版本和密码套件。 想要最大程度地提高连接性的客户端将包括过时的`TLS`版本和弱设计密码套件。 想要最大化安全性的严格客户端将仅限于最新的`TLS`版本和最强的密码套件。

特定的安全性与连接性决定由`ConnectionSpec`实施。 `OkHttp`包含四个内置连接规范：

* `RESTRICTED_TLS`是一种安全配置，旨在满足更严格的合规性要求。
* `MODERN_TLS`是连接到现代HTTPS服务器的安全配置。
* `COMPATIBLE_TLS`是一种安全配置，可连接到安全的HTTPS服务器，但不能连接到当前的HTTPS服务器。
* `CLEARTEXT`是用于`http://URL`的不安全配置。

这些宽松地遵循了Google云政策中设置的模型。 我们持续跟踪对此政策的更改。

默认情况下，OkHttp将尝试建立`MODERN_TLS`连接。 但是，如果现代配置失败，则可以通过配置客户端连接规范来允许回退到`COMPATIBLE_TLS`连接。

```java
OkHttpClient client = new OkHttpClient.Builder()
    .connectionSpecs(Arrays.asList(ConnectionSpec.MODERN_TLS, ConnectionSpec.COMPATIBLE_TLS))
    .build();
```

每个规范中的TLS版本和密码套件可随每个发行版而更改。 例如，在`OkHttp 2.2`中，为了响应`POODLE`攻击，我们放弃了对`SSL 3.0`的支持。 在`OkHttp 2.3`中，我们放弃了对`RC4`的支持。 **与桌面Web浏览器一样，保持OkHttp的最新状态是确保安全的最佳方法。**

您可以使用一组自定义的`TLS`版本和密码套件来构建自己的连接规范。 例如，此配置仅限于三个备受推崇的密码套件。 它的缺点是它需要`Android 5.0+`和类似的当前Web服务器。

```java
ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
    .tlsVersions(TlsVersion.TLS_1_2)
    .cipherSuites(
          CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM_SHA256)
    .build();

OkHttpClient client = new OkHttpClient.Builder()
    .connectionSpecs(Collections.singletonList(spec))
    .build();
```

## 调试TLS握手失败

TLS握手要求客户端和服务器共享一个通用的`TLS`版本和密码套件。 这取决于`JVM`或`Android`版本，`OkHttp`版本以及`Web`服务器配置。 如果没有通用的密码套件和`TLS`版本，您的呼叫将失败，如下所示：

```java
Caused by: javax.net.ssl.SSLProtocolException: SSL handshake aborted: ssl=0x7f2719a89e80:
    Failure in SSL library, usually a protocol error
        error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake 
        failure (external/openssl/ssl/s23_clnt.c:770 0x7f2728a53ea0:0x00000000)
    at com.android.org.conscrypt.NativeCrypto.SSL_do_handshake(Native Method)
```

您可以使用`Qualys SSL Labs`检查Web服务器的配置。 此处跟踪`OkHttp`的TLS配置历史记录。

预期将在较旧的`Android`设备上安装的应用程序应考虑采用`Google Play`服务的`ProviderInstaller`。 这将提高用户的安全性并增强与Web服务器的连接。

## 证书固定

默认情况下，`OkHttp`信任主机平台的证书颁发机构。 此策略可最大程度地提高连接性，但会受到诸如`2011 DigiNotar`攻击等证书颁发机构的攻击。 它还假定您的`HTTPS`服务器的证书是由证书颁发机构签名的。

使用`CertificatePinner`限制受信任的证书和证书颁发机构。 证书固定可提高安全性，但会限制您的服务器团队更新其TLS证书的能力。 **没有服务器的TLS管理员的支持，请勿使用证书固定！**

```java
 private final OkHttpClient client = new OkHttpClient.Builder()
      .certificatePinner(
          new CertificatePinner.Builder()
              .add("publicobject.com", "sha256/afwiKY3RxoMmLkuRW1l7QsPZTJPwDS2pdDROQjXw8ig=")
              .build())
      .build();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://publicobject.com/robots.txt")
        .build();

    try (Response response = client.newCall(request).execute()) {
      if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

      for (Certificate certificate : response.handshake().peerCertificates()) {
        System.out.println(CertificatePinner.pin(certificate));
      }
    }
  }
```

## 自定义可信证书

完整的代码示例显示了如何用您自己的证书集替换主机平台的证书颁发机构。 **如上所述，如果没有服务器的TLS管理员的祝福，请不要使用自定义证书！**

```java
  private final OkHttpClient client;

  public CustomTrust() {
    X509TrustManager trustManager;
    SSLSocketFactory sslSocketFactory;
    try {
      trustManager = trustManagerForCertificates(trustedCertificatesInputStream());
      SSLContext sslContext = SSLContext.getInstance("TLS");
      sslContext.init(null, new TrustManager[] { trustManager }, null);
      sslSocketFactory = sslContext.getSocketFactory();
    } catch (GeneralSecurityException e) {
      throw new RuntimeException(e);
    }

    client = new OkHttpClient.Builder()
        .sslSocketFactory(sslSocketFactory, trustManager)
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://publicobject.com/helloworld.txt")
        .build();

    Response response = client.newCall(request).execute();
    System.out.println(response.body().string());
  }

  private InputStream trustedCertificatesInputStream() {
    ... // Full source omitted. See sample.
  }

  public SSLContext sslContextForTrustedCertificates(InputStream in) {
    ... // Full source omitted. See sample.
  }
```

### 设置信任所有证书

```java
OkHttpClient.Builder hcBuilder = new OkHttpClient.Builder();
try {
    X509TrustManager x509TrustManager = new X509TrustManager() {
        @Override
        public void checkClientTrusted(java.security.cert.X509Certificate[] chain, String authType) throws CertificateException {
        }

        @Override
        public void checkServerTrusted(java.security.cert.X509Certificate[] chain, String authType) throws CertificateException {
        }

        @Override
        public java.security.cert.X509Certificate[] getAcceptedIssuers() {
            return new java.security.cert.X509Certificate[]{};
        }
    };
    final TrustManager[] trustAllCerts = new TrustManager[]{
        x509TrustManager
    };
    HostnameVerifier hostnameVerifier = new HostnameVerifier() {
        @Override
        public boolean verify(String hostname, SSLSession session) {
            return true;
        }
    };
    final SSLContext sslContext = SSLContext.getInstance("SSL");
    sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
    final SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();
    hcBuilder.sslSocketFactory(sslSocketFactory, x509TrustManager)
        .hostnameVerifier(hostnameVerifier);
}catch (Exception e){
    logger.error("ssl init fail.err={}",e.getMessage(),e);
}
```

