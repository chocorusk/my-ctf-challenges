# ChaChaCha

## 解法

ChaCha20はストリーム暗号とよばれる種類の暗号です。ストリーム暗号は、鍵から鍵ストリーム (keystream) とよばれる擬似ランダムなバイト列を計算し、平文とのXORを取ることで暗号文を生成します。つまり、暗号化の仕組みは以下のようになっています。

```python
def xor(a, b):
    return bytes(a[i] ^ b[i] for i in range(len(a)))

def get_keystream(key, nonce):
    ...(複雑な計算)
    return 擬似ランダムな長さ無限のバイト列

def encrypt(plaintext):
    keystream = get_keystream(key, nonce)
    return xor(plaintext, keystream[:len(plaintext)])
```

よって、XORの性質から、平文と対応する暗号文が既知の場合、keystream (の先頭部分) は平文と暗号文をXORすることで得られます。また、暗号文と暗号化に使われたkeystreamが既知の場合、平文は暗号文とkeystreamをXORすることで逆算できます。

この問題では、keyとnonceは固定なので、2回の暗号化処理におけるkeystreamは同じです。よって、`msg` と `msg` の暗号文 `encrypted msg` をXORしてkeystreamを計算し、`encrypted flag` にkeystreamをXORすることでフラグを復号できます。

```python
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

msg = b"Daily AlpacaHack is a daily CTF challenge with a fun new puzzle every day."
keystream = xor(encrypted_msg, msg)
print(xor(encrypted_flag, keystream))
```

Flag: `Alpaca{le7's_63t_reven6e_4t_th3_n3xt_SECCON!}`

ちなみに、問題文の "Nostalgic" はSECCON 14 Qualsで出題された問題です。ChaCha20と、Poly1305というメッセージ認証コード (MAC) を組み合わせた認証付き暗号が題材の問題で、12チームしか解けなかった難問です。ぜひcryptoを勉強して、自信がついてきたらチャレンジしてみてください。
